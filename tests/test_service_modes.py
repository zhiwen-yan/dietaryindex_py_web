from __future__ import annotations

from pathlib import Path
from time import sleep
import json

import numpy as np
import pandas as pd
from fastapi.testclient import TestClient

import dietaryindex.service.compute as compute_service
from dietaryindex.service import get_index_detail, run_compute
from dietaryindex.service.compute import run_multi_cycle_compute
from dietaryindex.service.results import build_result_payload
from dietaryindex_api.app import app


def test_index_detail_includes_mode_specs():
    detail = get_index_detail("PHDI")
    assert "mode_specs" in detail
    assert "nhanes_fped" in detail["mode_specs"]
    assert any(item["key"] == "nutrient_path" for item in detail["mode_specs"]["nhanes_fped"])


def test_run_compute_block_mode(tmp_path: Path):
    csv_path = tmp_path / "block_minimal.csv"
    csv_path.write_text(
        "\n".join(
            [
                "respondent_id,fruit_fruit_juice,vegetable,whole_grain,legumes,nuts,fish,red_processed_meat,mon_sat_fat_ratio,alcohol",
                "1,3.0,4.0,2.0,1.0,0.5,1.2,0.8,1.8,0.5",
                "2,1.5,2.0,1.0,0.2,0.1,0.3,1.5,1.1,0.1",
            ]
        ),
        encoding="utf-8",
    )

    result = run_compute(
        index_key="MED",
        mode="block",
        file_path=str(csv_path),
        output_dir=tmp_path / "out",
    )

    assert result["index_key"] == "MED"
    assert result["mode"] == "block"
    assert result["rows"] == 2
    assert "MED_ALL" in result["columns"]
    assert result["mapping_used"]["fruit_fruit_juice"] == "fruit_fruit_juice"


def test_nutrient_indices_run_for_questionnaire_source_modes(tmp_path: Path):
    csv_path = tmp_path / "standard_nutrients.csv"
    csv_path.write_text(
        "\n".join(
            [
                "UserName,KCAL,PROT,CARB,TFIBE,TFAT,SFAT,MFAT,PFAT,CHOLE,ALCO,CAFF,FOLA,NIA,MG,IRON,ZINC,SELE,THIA,RIBO,VITB6,VITB12,VITC,VITD,VITA_RAE,ATOC,CALC,POTA,PHOS,ASUG,SODI,ACAR,BCAR,CRYP,LYCO,LUT_ZEA,P182,P183,P204,P226,P205,P225",
                "P001,1800,70,220,28,60,18,20,17,220,5,120,400,16,320,12,11,70,1.2,1.4,1.5,3.0,85,12,750,14,900,3500,1200,35,1900,500,3500,180,3200,2200,12,2.0,0.2,0.8,0.3,0.2",
                "P002,2100,82,250,32,72,22,25,20,250,8,160,450,18,360,14,13,82,1.4,1.6,1.8,3.5,95,14,820,16,1000,3900,1350,42,2200,620,3900,210,3600,2500,15,2.4,0.3,1.0,0.4,0.3",
            ]
        ),
        encoding="utf-8",
    )

    indices = ("FISI", "NRF", "NAR", "MAR", "INQ", "PRAL", "NEAP", "CDAI")
    for index_key in indices:
        for mode in ("asa24", "dhq3", "block"):
            result = run_compute(
                index_key=index_key,
                mode=mode,
                file_path=csv_path,
                output_dir=tmp_path / "out" / index_key / mode,
            )
            assert result["rows"] == 2
            assert result["mode"] == mode


def test_api_compute_accepts_upload_ids_for_multifile_mode():
    client = TestClient(app)

    upload1 = client.post(
        "/v1/uploads",
        files={"file": ("fake_tot.csv", b"SEQN,DR1TKCAL\n1,2000\n", "text/csv")},
    )
    upload2 = client.post(
        "/v1/uploads",
        files={"file": ("fake_demo.csv", b"SEQN,RIDAGEYR\n1,30\n", "text/csv")},
    )
    assert upload1.status_code == 200
    assert upload2.status_code == 200

    response = client.post(
        "/v1/compute",
        json={
            "index_key": "DII",
            "mode": "nhanes_fped",
            "upload_ids": {
                "nutrient_path": upload1.json()["upload_id"],
                "demo_path": upload2.json()["upload_id"],
            },
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["mode"] == "nhanes_fped"
    assert payload["status"] in {"queued", "running", "succeeded", "failed"}


def test_api_compute_accepts_cycles_without_top_level_upload_ids():
    client = TestClient(app)
    upload = client.post(
        "/v1/uploads",
        files={
            "file": (
                "fake_tot.csv",
                b"SEQN,DR1DRSTZ,DR1TKCAL,DR1TPROT\n1,1,2000,70\n",
                "text/csv",
            )
        },
    )
    assert upload.status_code == 200

    response = client.post(
        "/v1/compute",
        json={
            "index_key": "DII",
            "mode": "nhanes_fped",
            "cycles": [
                {
                    "label": "2017-2018",
                    "upload_ids": {
                        "nutrient_path": upload.json()["upload_id"],
                    },
                }
            ],
        },
    )

    assert response.status_code == 200
    assert response.json()["mode"] == "nhanes_fped"


def test_multi_cycle_results_and_exports_are_sorted_chronologically(tmp_path: Path, monkeypatch):
    def fake_adapter(nutrient_path=None):
        return pd.DataFrame({"DII_ALL": [float(Path(nutrient_path).stem)]})

    monkeypatch.setitem(compute_service.ADAPTER_MAP, ("DII", "nhanes_fped"), fake_adapter)
    cycles = [
        {"label": "2017-2018", "file_paths": {"nutrient_path": "2017.csv"}},
        {"label": "2005-2006", "file_paths": {"nutrient_path": "2005.csv"}},
        {"label": "2011-2012", "file_paths": {"nutrient_path": "2011.csv"}},
    ]

    result = run_multi_cycle_compute(
        index_key="DII",
        mode="nhanes_fped",
        cycles=cycles,
        output_dir=tmp_path,
    )

    expected = ["2005-2006", "2011-2012", "2017-2018"]
    assert [row["NHANES_CYCLE"] for row in result["preview"]] == expected
    assert [cycle["label"] for cycle in result["mapping_used"]["cycles"]] == expected
    exported = pd.read_csv(result["files"]["csv_path"])
    assert exported["NHANES_CYCLE"].tolist() == expected


def test_service_fisi1_uses_bundled_food_database(tmp_path: Path):
    individual_path = tmp_path / "DR1IFF_J.csv"
    total_path = tmp_path / "DR1TOT_J.csv"
    pd.DataFrame(
        {
            "SEQN": [1, 2],
            "DR1IFDCD": [11000000.0, 11111000.0],
            "DR1IGRMS": [100.0, 100.0],
        }
    ).to_csv(individual_path, index=False)
    pd.DataFrame(
        {
            "SEQN": [1, 2],
            "DR1DRSTZ": [1, 1],
            "DR1TKCAL": [2000.0, 1800.0],
            "DR1TALCO": [0.0, 0.0],
        }
    ).to_csv(total_path, index=False)

    result = run_compute(
        index_key="FISI",
        mode="nhanes_fped",
        file_paths={
            "nutrient_path": total_path,
            "nutrient_ind_path": individual_path,
        },
        options={"fisi_variant": "fisi1"},
        output_dir=tmp_path / "results",
    )

    assert result["primary_output_column"] == "FISI1"
    assert result["rows"] == 2
    assert np.isclose(result["preview"][0]["FISI1"], -0.04799631)
    assert np.isclose(result["preview"][1]["FISI1"], -0.07751487)


def test_api_compute_status_and_download_do_not_expose_paths():
    client = TestClient(app)
    contents = "\n".join(
        [
            "respondent_id,fruit_fruit_juice,vegetable,whole_grain,legumes,nuts,fish,red_processed_meat,mon_sat_fat_ratio,alcohol",
            "1,3.0,4.0,2.0,1.0,0.5,1.2,0.8,1.8,0.5",
            "2,1.5,2.0,1.0,0.2,0.1,0.3,1.5,1.1,0.1",
        ]
    )
    upload = client.post(
        "/v1/uploads",
        files={"file": ("block.csv", contents.encode(), "text/csv")},
    )
    assert upload.status_code == 200

    submitted = client.post(
        "/v1/compute",
        json={
            "index_key": "MED",
            "mode": "block",
            "upload_id": upload.json()["upload_id"],
        },
    )
    assert submitted.status_code == 200
    job_id = submitted.json()["job_id"]

    payload = None
    for _ in range(100):
        status = client.get(f"/v1/jobs/{job_id}")
        assert status.status_code == 200
        payload = status.json()
        if payload["status"] in {"succeeded", "failed"}:
            break
        sleep(0.05)

    assert payload is not None
    assert payload["status"] == "succeeded", payload.get("error")
    assert "file_path" not in payload
    assert "file_paths" not in payload
    assert "files" not in payload["result"]
    assert payload["result"]["downloads"]["csv"].endswith("format=csv")

    downloaded = client.get(f"/v1/jobs/{job_id}/download", params={"format": "csv"})
    assert downloaded.status_code == 200
    assert "MED_ALL" in downloaded.text


def test_result_payload_serializes_nonfinite_values_as_null(tmp_path: Path):
    payload = build_result_payload(
        index_key="PHDI",
        mode="asa24",
        result=pd.DataFrame(
            {
                "PHDI_ALL": [np.nan, np.inf, -np.inf, 12.5],
                "ID": [1, 2, 3, 4],
            }
        ),
        output_dir=tmp_path,
        primary_output_column="PHDI_ALL",
    )

    assert [row["PHDI_ALL"] for row in payload["preview"]] == [None, None, None, 12.5]
    assert payload["summary_stats"]["count"] == 1
    assert payload["summary_stats"]["mean"] == 12.5
    json.dumps(payload, allow_nan=False)
