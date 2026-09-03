import assert from "node:assert/strict";
import { test } from "node:test";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import worker from "../src/index.js";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");

test("OpenCode relay forwards the session header and permits browser preflight", async () => {
  const realFetch = globalThis.fetch;
  let upstream;

  globalThis.fetch = async (input, init) => {
    upstream = {
      url: String(input),
      headers: new Headers(init?.headers),
    };
    return new Response("{}", {
      status: 200,
      headers: { "content-type": "application/json" },
    });
  };

  try {
    const request = new Request("https://proxy.test/v1/chat/completions", {
      method: "POST",
      headers: {
        Origin: "https://achappell.github.io",
        Authorization: "Bearer test-key",
        "Content-Type": "application/json",
        "x-opencode-session": "conversation-123",
      },
      body: "{}",
    });

    const response = await worker.fetch(request);
    assert.equal(response.status, 200);
    assert.equal(upstream.url, "https://opencode.ai/zen/go/v1/chat/completions");
    assert.equal(upstream.headers.get("x-opencode-session"), "conversation-123");

    const preflight = await worker.fetch(new Request("https://proxy.test/v1/chat/completions", {
      method: "OPTIONS",
      headers: {
        Origin: "https://achappell.github.io",
        "Access-Control-Request-Headers": "content-type,x-opencode-session",
      },
    }));
    assert.equal(preflight.status, 204);
    assert.match(preflight.headers.get("access-control-allow-headers"), /x-opencode-session/i);
  } finally {
    globalThis.fetch = realFetch;
  }
});

test("every Character Chat OpenCode caller sends a session header", () => {
  for (const file of ["joke-lab.html", "kids-chatbot.html", "mad-libs.html", "story-builder.html"]) {
    const source = fs.readFileSync(path.join(root, file), "utf8");
    assert.match(source, /headers\[(['"])x-opencode-session\1\]\s*=\s*window\.getOpenCodeSessionId\(\)/, file);
  }
});
