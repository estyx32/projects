// Command center client. Fragments are server-rendered and autoescaped; this file only
// refreshes them, applies meter widths (CSP forbids inline styles) and sends actions.
(() => {
  const csrf = document.querySelector('meta[name="csrf-token"]').content;
  const sections = [...document.querySelectorAll("[data-section]")];
  const timers = new Map();

  function applyWidths(root) {
    root.querySelectorAll("[data-width]").forEach((el) => {
      el.style.width = el.dataset.width + "%";
    });
  }

  function openDetailsIndexes(root) {
    return [...root.querySelectorAll("details")].map((d, i) => (d.open ? i : -1)).filter((i) => i >= 0);
  }

  async function refresh(name) {
    const el = document.getElementById(name);
    if (!el || document.hidden) return;
    try {
      const res = await fetch("/fragment/" + name, { cache: "no-store" });
      if (!res.ok) throw new Error("HTTP " + res.status);
      const html = await res.text();
      const open = openDetailsIndexes(el);
      el.innerHTML = html;
      el.querySelectorAll("details").forEach((d, i) => { d.open = open.includes(i); });
      applyWidths(el);
      el.classList.remove("stale-ui");
    } catch (err) {
      el.classList.add("stale-ui"); // keep showing the last good data, but mark it
    }
  }

  function refreshAll() { sections.forEach((s) => refresh(s.id)); }

  function schedule() {
    sections.forEach((s) => {
      const ms = Number(s.dataset.interval) || 10000;
      timers.set(s.id, setInterval(() => refresh(s.id), ms));
    });
  }

  function toast(message, bad) {
    let box = document.getElementById("toast");
    if (!box) {
      box = document.createElement("div");
      box.id = "toast";
      box.setAttribute("role", "status");
      box.setAttribute("aria-live", "polite");
      document.body.appendChild(box);
    }
    box.textContent = message;
    box.className = bad ? "bad" : "ok";
    clearTimeout(box._t);
    box._t = setTimeout(() => { box.className = ""; box.textContent = ""; }, 6000);
  }

  async function post(url, body) {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-CSRF-Token": csrf },
      body: JSON.stringify(body || {}),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.detail || data.error || "HTTP " + res.status);
    return data;
  }

  document.addEventListener("click", async (ev) => {
    const btn = ev.target.closest("button[data-action]");
    if (!btn || btn.disabled) return;
    btn.disabled = true;
    try {
      if (btn.dataset.action === "kill") {
        const on = btn.dataset.on === "true";
        if (!on && !confirm("Resume trading? The engine will start accepting approvals again.")) return;
        await post("/api/kill", { on });
        toast(on ? "Kill switch ON. Nothing will be approved." : "Kill switch off.", false);
      } else if (btn.dataset.action === "decide") {
        const data = await post("/api/proposals/" + btn.dataset.id + "/" + btn.dataset.verb);
        if (data.status === "blocked") toast("Blocked by the risk gate at approval time. See activity.", true);
        else toast("Proposal " + data.status + ".", false);
      }
      refreshAll();
    } catch (err) {
      toast("Action failed: " + err.message, true);
    } finally {
      btn.disabled = false;
    }
  });

  document.addEventListener("visibilitychange", () => { if (!document.hidden) refreshAll(); });
  applyWidths(document);
  schedule();
})();
