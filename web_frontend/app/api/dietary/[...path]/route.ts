import { NextRequest } from "next/server";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

type RouteContext = { params: Promise<{ path: string[] }> };

async function proxy(request: NextRequest, context: RouteContext): Promise<Response> {
  const { path } = await context.params;
  const base = process.env.DIETARYINDEX_API_INTERNAL_URL ?? "http://127.0.0.1:8000";
  const upstreamUrl = new URL(`/${path.map(encodeURIComponent).join("/")}`, base);
  request.nextUrl.searchParams.forEach((value: string, key: string) =>
    upstreamUrl.searchParams.append(key, value),
  );

  const headers = new Headers(request.headers);
  headers.delete("host");
  headers.delete("connection");
  headers.delete("content-length");
  const apiKey = process.env.DIETARYINDEX_API_KEY?.trim();
  if (apiKey) headers.set("x-api-key", apiKey);

  const hasBody = request.method !== "GET" && request.method !== "HEAD";
  const upstream = await fetch(upstreamUrl, {
    method: request.method,
    headers,
    body: hasBody ? await request.arrayBuffer() : undefined,
    cache: "no-store",
    redirect: "manual",
  });

  const responseHeaders = new Headers(upstream.headers);
  responseHeaders.delete("content-encoding");
  responseHeaders.delete("content-length");
  return new Response(upstream.body, {
    status: upstream.status,
    statusText: upstream.statusText,
    headers: responseHeaders,
  });
}

export const GET = proxy;
export const POST = proxy;
