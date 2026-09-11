import { NextResponse } from "next/server";

export const dynamic = "force-dynamic";

export async function GET() {
  const desktopMode = process.env.DIETARYINDEX_DESKTOP_MODE === "1";
  return NextResponse.json({
    desktopMode,
    apiBaseUrl: desktopMode
      ? process.env.DIETARYINDEX_API_INTERNAL_URL ?? null
      : null,
  });
}
