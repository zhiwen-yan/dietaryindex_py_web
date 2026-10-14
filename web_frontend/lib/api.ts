import type { Job } from "@/lib/types";

export class ApiError extends Error {
  status: number;

  constructor(status: number, message: string) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

export async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`/api/dietary${path}`, {
    ...init,
    cache: "no-store",
  });

  if (!response.ok) {
    let message = `${response.status} ${response.statusText}`;
    try {
      const payload = (await response.json()) as { detail?: string };
      if (payload.detail) message = payload.detail;
    } catch {
      // Keep the HTTP status text when the upstream body is not JSON.
    }
    throw new ApiError(response.status, message);
  }

  return (await response.json()) as T;
}

export function proxiedDownloadUrl(path: string): string {
  return `/api/dietary${path}`;
}

export async function waitForJob(
  jobId: string,
  onUpdate: (job: Job) => void,
  timeoutMs = 120_000,
): Promise<Job> {
  const started = Date.now();
  while (Date.now() - started < timeoutMs) {
    const job = await apiFetch<Job>(`/v1/jobs/${jobId}`);
    onUpdate(job);
    if (job.status === "succeeded" || job.status === "failed") return job;
    await new Promise((resolve) => window.setTimeout(resolve, 800));
  }
  throw new Error("计算等待超时，请稍后在任务记录中查询结果。");
}
