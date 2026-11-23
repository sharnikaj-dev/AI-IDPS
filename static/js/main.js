(function () {
  const page = document.body.dataset.page || "";
  const sidebar = document.getElementById("sidebar");
  const menuToggle = document.getElementById("menuToggle");
  const globalStatus = document.getElementById("globalMonitorStatus");

  if (menuToggle && sidebar) {
    menuToggle.addEventListener("click", () => {
      sidebar.classList.toggle("open");
    });
  }

  function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text == null ? "" : String(text);
    return div.innerHTML;
  }

  function severityBadge(sev) {
    if (sev === "HIGH") return '<span class="badge badge-danger">HIGH</span>';
    if (sev === "MEDIUM") return '<span class="badge badge-warning">MEDIUM</span>';
    return '<span class="badge badge-info">LOW</span>';
  }

  function actionBadge(action) {
    if (action === "Blocked") return '<span class="badge badge-danger">Blocked</span>';
    if (action === "Rate-limited") return '<span class="badge badge-warning">Rate-limited</span>';
    return '<span class="badge badge-success">Logged</span>';
  }

  function predictionBadge(pred) {
    if (pred === "Normal") return '<span class="badge badge-success">Normal</span>';
    return `<span class="badge badge-danger">${escapeHtml(pred)}</span>`;
  }

  function updateGlobalStatus(running) {
    if (!globalStatus) return;
    globalStatus.textContent = running ? "Monitoring Active" : "Stopped";
    globalStatus.className = `status-pill ${running ? "status-running" : "status-stopped"}`;
  }

  async function startReplay(options = {}) {
    const res = await fetch("/api/start", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(options),
    });
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.error || "Failed to start monitoring");
    }
    updateGlobalStatus(true);
    return data;
  }

  async function stopReplay() {
    const res = await fetch("/api/stop", { method: "POST" });
    const data = await res.json();
    updateGlobalStatus(false);
    return data;
  }

  // ---------------- Start Monitoring Page ----------------
  if (page === "monitor") {
    const startBtn = document.getElementById("startMonitorBtn");
    const stopBtn = document.getElementById("stopMonitorBtn");
    const feedback = document.getElementById("monitorFeedback");
    const progressText = document.getElementById("monitorProgressText");
    const progressBar = document.getElementById("monitorProgressBar");

    function showFeedback(msg, isError) {
      feedback.textContent = msg;
      feedback.className = `alert-banner ${isError ? "alert-error" : "alert-success"}`;
    }

    if (startBtn) {
      startBtn.addEventListener("click", async () => {
        try {
          const payload = {
            speed_ms: Number(document.getElementById("speedMs").value || 1000),
            batch_size: Number(document.getElementById("batchSize").value || 5),
            block_threshold: Number(document.getElementById("blockThreshold").value || 0.9),
            limit_threshold: Number(document.getElementById("limitThreshold").value || 0.6),
            reset: Boolean(document.getElementById("resetReplay").checked),
          };
          const data = await startReplay(payload);
          showFeedback(
            `Monitoring started (${data.total} records queued at ${data.speed_ms} ms interval).`,
            false
          );
          if (progressText && progressBar) {
            progressText.textContent = `${data.pos} / ${data.total}`;
            const pct = data.total ? (data.pos / data.total) * 100 : 0;
            progressBar.style.width = `${pct}%`;
          }
        } catch (err) {
          showFeedback(err.message, true);
        }
      });
    }

    if (stopBtn) {
      stopBtn.addEventListener("click", async () => {
        const data = await stopReplay();
        showFeedback(`Monitoring stopped at record ${data.pos} / ${data.total}.`, false);
      });
    }
  }

  // ---------------- Dashboard Page ----------------
  let timelineChart = null;
  let attackChart = null;

  function initDashboardCharts() {
    const tCanvas = document.getElementById("trafficTimelineChart");
    const aCanvas = document.getElementById("attackTypeChart");
    if (!tCanvas || !aCanvas || typeof Chart === "undefined") return;

    timelineChart = new Chart(tCanvas.getContext("2d"), {
      type: "line",
      data: {
        labels: [],
        datasets: [
          {
            label: "Normal",
            data: [],
            borderColor: "#22c55e",
            backgroundColor: "rgba(34, 197, 94, 0.15)",
            tension: 0.3,
            fill: true,
          },
          {
            label: "Attack",
            data: [],
            borderColor: "#ef4444",
            backgroundColor: "rgba(239, 68, 68, 0.18)",
            tension: 0.3,
            fill: true,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { labels: { color: "#e2e8f0" } } },
        scales: {
          x: { ticks: { color: "#94a3b8" }, grid: { color: "rgba(148,163,184,0.1)" } },
          y: { beginAtZero: true, ticks: { color: "#94a3b8" }, grid: { color: "rgba(148,163,184,0.1)" } },
        },
      },
    });

    attackChart = new Chart(aCanvas.getContext("2d"), {
      type: "bar",
      data: {
        labels: ["DoS", "Probe", "R2L", "U2R"],
        datasets: [
          {
            label: "Detected Threats",
            data: [0, 0, 0, 0],
            backgroundColor: ["#ef4444", "#f59e0b", "#38bdf8", "#a855f7"],
            borderRadius: 6,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: { ticks: { color: "#94a3b8" }, grid: { display: false } },
          y: { beginAtZero: true, ticks: { color: "#94a3b8" }, grid: { color: "rgba(148,163,184,0.1)" } },
        },
      },
    });
  }

  async function refreshDashboard() {
    const res = await fetch("/api/stats");
    if (!res.ok) return;
    const stats = await res.json();

    updateGlobalStatus(stats.running);
    document.getElementById("kpiFlows").textContent = stats.flows_analysed.toLocaleString();
    document.getElementById("kpiThreats").textContent = stats.threats_detected.toLocaleString();
    document.getElementById("kpiBlocked").textContent = stats.blocked_ips.toLocaleString();
    document.getElementById("kpiAccuracy").textContent = `${stats.model_accuracy}%`;
    document.getElementById("dashProgressInfo").textContent =
      `Processed: ${stats.position} / ${stats.total}`;

    if (timelineChart && stats.timeline) {
      timelineChart.data.labels = stats.timeline.labels;
      timelineChart.data.datasets[0].data = stats.timeline.normal;
      timelineChart.data.datasets[1].data = stats.timeline.attack;
      timelineChart.update("none");
    }

    if (attackChart && stats.attack_counts) {
      attackChart.data.datasets[0].data = [
        stats.attack_counts.DoS || 0,
        stats.attack_counts.Probe || 0,
        stats.attack_counts.R2L || 0,
        stats.attack_counts.U2R || 0,
      ];
      attackChart.update("none");
    }

    const tbody = document.getElementById("dashRecentAlerts");
    if (tbody) {
      if (!stats.recent_alerts || stats.recent_alerts.length === 0) {
        tbody.innerHTML =
          '<tr><td colspan="8" class="empty-cell">No alerts recorded yet. Start monitoring to analyse traffic.</td></tr>';
      } else {
        tbody.innerHTML = stats.recent_alerts
          .map(
            (a) => `
          <tr>
            <td class="mono">A-${1000 + a.alert_id}</td>
            <td>${escapeHtml(a.alert_time)}</td>
            <td class="mono">${escapeHtml(a.src_ip)}</td>
            <td>${escapeHtml(a.service)}</td>
            <td><span class="badge badge-info">${escapeHtml(a.attack_type)}</span></td>
            <td>${(Number(a.confidence) * 100).toFixed(1)}%</td>
            <td>${severityBadge(a.severity)}</td>
            <td>${actionBadge(a.action_taken)}</td>
          </tr>`
          )
          .join("");
      }
    }
    return stats;
  }

  if (page === "dashboard") {
    initDashboardCharts();
    refreshDashboard();

    const startBtn = document.getElementById("dashStartBtn");
    const stopBtn = document.getElementById("dashStopBtn");

    if (startBtn) {
      startBtn.addEventListener("click", async () => {
        await startReplay();
        await refreshDashboard();
      });
    }
    if (stopBtn) {
      stopBtn.addEventListener("click", async () => {
        await stopReplay();
        await refreshDashboard();
      });
    }

    setInterval(async () => {
      const nextRes = await fetch("/api/next");
      if (nextRes.ok) {
        await refreshDashboard();
      }
    }, 1200);
  }

  // ---------------- Live Monitor Page ----------------
  function prependLiveRow(tbody, r) {
    const emptyRow = document.getElementById("liveEmptyRow");
    if (emptyRow) emptyRow.remove();

    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${escapeHtml(r.time)}</td>
      <td class="mono">${escapeHtml(r.src_ip)}</td>
      <td class="mono">${escapeHtml(r.dst_ip)}</td>
      <td>${escapeHtml(r.protocol)}</td>
      <td>${escapeHtml(r.service)}</td>
      <td>${predictionBadge(r.prediction)}</td>
      <td>${Number(r.confidence).toFixed(1)}%</td>
      <td>${actionBadge(r.action)}</td>
    `;
    tbody.prepend(tr);
    while (tbody.rows.length > 25) {
      tbody.deleteRow(-1);
    }
  }

  if (page === "live") {
    const tbody = document.getElementById("liveBody");
    const counter = document.getElementById("liveCounter");
    const startBtn = document.getElementById("liveStartBtn");
    const stopBtn = document.getElementById("liveStopBtn");

    if (startBtn) {
      startBtn.addEventListener("click", async () => {
        await startReplay();
      });
    }
    if (stopBtn) {
      stopBtn.addEventListener("click", async () => {
        await stopReplay();
      });
    }

    setInterval(async () => {
      const res = await fetch("/api/next");
      if (!res.ok) return;
      const data = await res.json();
      updateGlobalStatus(data.running);
      if (counter && data.total) {
        counter.textContent = `Processed: ${data.position} / ${data.total}`;
      }
      if (tbody && data.results && data.results.length > 0) {
        data.results.forEach((r) => prependLiveRow(tbody, r));
      }
    }, 1000);
  }

  // ---------------- Alerts Page ----------------
  if (page === "alerts") {
    let currentSeverity = "ALL";
    const filterGroup = document.getElementById("severityFilterGroup");
    const tbody = document.getElementById("alertsTableBody");

    async function loadAlerts(severity) {
      const res = await fetch(`/api/alerts?severity=${encodeURIComponent(severity)}`);
      if (!res.ok) return;
      const data = await res.json();
      if (!data.alerts || data.alerts.length === 0) {
        tbody.innerHTML =
          '<tr><td colspan="8" class="empty-cell">No alerts found for this filter.</td></tr>';
        return;
      }
      tbody.innerHTML = data.alerts
        .map(
          (a) => `
        <tr>
          <td class="mono">A-${1000 + a.alert_id}</td>
          <td>${escapeHtml(a.alert_time)}</td>
          <td class="mono">${escapeHtml(a.src_ip)}</td>
          <td>${escapeHtml(a.protocol)} / ${escapeHtml(a.service)}</td>
          <td><span class="badge badge-info">${escapeHtml(a.attack_type)}</span></td>
          <td>${(Number(a.confidence) * 100).toFixed(1)}%</td>
          <td>${severityBadge(a.severity)}</td>
          <td>${actionBadge(a.action_taken)}</td>
        </tr>`
        )
        .join("");
    }

    if (filterGroup) {
      filterGroup.addEventListener("click", (e) => {
        const btn = e.target.closest("button[data-severity]");
        if (!btn) return;
        currentSeverity = btn.dataset.severity;
        filterGroup.querySelectorAll("button").forEach((b) => {
          b.className = `btn btn-sm ${b === btn ? "btn-primary" : "btn-outline"}`;
        });
        loadAlerts(currentSeverity);
      });
    }

    setInterval(() => loadAlerts(currentSeverity), 3000);
  }

  // ---------------- Blocked IPs Page ----------------
  if (page === "blocked") {
    const tbody = document.getElementById("blockedTableBody");
    const refreshBtn = document.getElementById("refreshBlockedBtn");

    async function loadBlocked() {
      const res = await fetch("/api/blocked");
      if (!res.ok) return;
      const data = await res.json();
      if (!data.blocked || data.blocked.length === 0) {
        tbody.innerHTML =
          '<tr><td colspan="6" class="empty-cell">No IP addresses have been blocked yet.</td></tr>';
        return;
      }
      tbody.innerHTML = data.blocked
        .map((b) => {
          const isBlocked = b.status === "Blocked";
          return `
          <tr data-block-id="${b.block_id}">
            <td class="mono">B-${b.block_id}</td>
            <td class="mono">${escapeHtml(b.ip_address)}</td>
            <td><span class="badge badge-info">${escapeHtml(b.reason)}</span></td>
            <td>${escapeHtml(b.blocked_at)}</td>
            <td><span class="badge ${isBlocked ? "badge-danger" : "badge-success"}">${escapeHtml(b.status)}</span></td>
            <td>
              ${
                isBlocked
                  ? `<button type="button" class="btn btn-outline btn-sm unblock-btn" data-id="${b.block_id}">Unblock</button>`
                  : `<button type="button" class="btn btn-danger btn-sm reblock-btn" data-id="${b.block_id}">Re-block</button>`
              }
            </td>
          </tr>`;
        })
        .join("");
    }

    if (tbody) {
      tbody.addEventListener("click", async (e) => {
        const unblockBtn = e.target.closest(".unblock-btn");
        const reblockBtn = e.target.closest(".reblock-btn");
        if (unblockBtn) {
          await fetch(`/api/unblock/${unblockBtn.dataset.id}`, { method: "POST" });
          await loadBlocked();
        } else if (reblockBtn) {
          await fetch(`/api/reblock/${reblockBtn.dataset.id}`, { method: "POST" });
          await loadBlocked();
        }
      });
    }

    if (refreshBtn) {
      refreshBtn.addEventListener("click", loadBlocked);
    }
  }

  // ---------------- Reports Page ----------------
  if (page === "reports") {
    const form = document.getElementById("reportFilterForm");
    const startInput = document.getElementById("reportStart");
    const endInput = document.getElementById("reportEnd");
    const csvLink = document.getElementById("downloadCsvBtn");
    const tbody = document.getElementById("reportTableBody");

    async function loadReport() {
      const start = startInput.value;
      const end = endInput.value;
      if (csvLink) {
        csvLink.href = `/api/report/csv?start=${encodeURIComponent(start)}&end=${encodeURIComponent(end)}`;
      }
      const res = await fetch(
        `/api/report?start=${encodeURIComponent(start)}&end=${encodeURIComponent(end)}`
      );
      if (!res.ok) return;
      const rep = await res.json();

      document.getElementById("repFlows").textContent = rep.total_flows.toLocaleString();
      document.getElementById("repThreats").textContent = rep.total_threats.toLocaleString();
      document.getElementById("repBlocked").textContent = rep.total_blocked.toLocaleString();
      document.getElementById("repLimitedLogged").textContent =
        `${rep.total_rate_limited} / ${rep.total_logged}`;

      tbody.innerHTML = rep.breakdown
        .map(
          (row) => `
        <tr>
          <td><strong>${escapeHtml(row.attack_type)}</strong></td>
          <td>${row.detected}</td>
          <td><span class="badge badge-danger">${row.blocked}</span></td>
          <td><span class="badge badge-warning">${row.rate_limited}</span></td>
          <td><span class="badge badge-success">${row.logged}</span></td>
        </tr>`
        )
        .join("");
    }

    if (form) {
      form.addEventListener("submit", (e) => {
        e.preventDefault();
        loadReport();
      });
    }
    loadReport();
  }

  // Sync topbar status pill once on page load
  if (globalStatus) {
    fetch("/api/stats")
      .then((r) => (r.ok ? r.json() : null))
      .then((s) => {
        if (s) updateGlobalStatus(s.running);
      })
      .catch(() => {});
  }
})();