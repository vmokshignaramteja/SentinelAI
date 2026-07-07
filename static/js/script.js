document.addEventListener("DOMContentLoaded", () => {

    console.log("SentinelAI Loaded");

    const glow = document.querySelector(".cursor-glow");

    document.addEventListener("mousemove", (e) => {
        if (glow) {
            glow.style.left = e.clientX + "px";
            glow.style.top = e.clientY + "px";
        }
    });

});

async function loadPackets() {

    const response = await fetch("/packets");
    const packets = await response.json();

    const tbody = document.querySelector("#packetTable tbody");

    tbody.innerHTML = "";

   const search = document
    .getElementById("searchInput")
    ?.value.toLowerCase() || "";

packets
.filter(packet =>
    packet.src.toLowerCase().includes(search) ||
    packet.dst.toLowerCase().includes(search) ||
    packet.protocol.toLowerCase().includes(search) ||
    packet.time.toLowerCase().includes(search)
)
.forEach(packet => {

        const protocol = packet.protocol.toLowerCase();

        tbody.innerHTML += `
        <tr>
            <td>${packet.time}</td>
            <td class="ip">${packet.src}</td>
            <td class="ip">${packet.dst}</td>
            <td>
                <span class="protocol ${protocol}">
                    ${packet.protocol}
                </span>
            </td>
            <td>
                <span class="size">
                    ${packet.size} B
                </span>
            </td>
        </tr>
        `;

    });

}

function animateValue(id, end) {

    const element = document.getElementById(id);

    if (!element) return;

    const start = parseInt(element.innerText) || 0;

    const duration = 500;
    const increment = (end - start) / 30;

    let current = start;

    const timer = setInterval(() => {

        current += increment;

        if (
            (increment > 0 && current >= end) ||
            (increment < 0 && current <= end)
        ) {
            current = end;
            clearInterval(timer);
        }

        element.innerText = Math.round(current);

    }, duration / 30);

}

async function loadStats() {

    console.log("Loading stats...");

    const response = await fetch("/stats");
    const stats = await response.json();

    console.log(stats);

    animateValue("totalPackets", stats.total);
    animateValue("tcpPackets", stats.tcp);
    animateValue("udpPackets", stats.udp);
    animateValue("uniqueIPs", stats.unique_ips);

}

loadPackets();
loadStats();
loadAlerts();

setInterval(loadPackets, 2000);
setInterval(loadStats, 2000);
setInterval(loadAlerts, 2000);

console.log("Bottom reached");

console.log("Bottom reached");
// ===========================
// LIVE SECURITY ALERTS
// ===========================

async function loadAlerts() {

    const response = await fetch("/alerts");
    const alerts = await response.json();

    const tbody = document.querySelector("#alertsTable tbody");

    if (!tbody) return;

    tbody.innerHTML = "";

    alerts.forEach(alert => {

        let color = "#22c55e";

        if (alert.level === "High") {
            color = "#ef4444";
        }
        else if (alert.level === "Medium") {
            color = "#f59e0b";
        }

        tbody.innerHTML += `
        <tr>
            <td>${alert.time}</td>
            <td>${alert.ip}</td>
            <td style="color:${color};font-weight:bold;">
                ${alert.level}
            </td>
            <td>${alert.message}</td>
        </tr>
        `;

    });

}
// ===========================
// SEARCH PACKETS
// ===========================

const searchInput = document.getElementById("searchInput");

if (searchInput) {

    searchInput.addEventListener("keyup", function () {

        const filter = this.value.toLowerCase();

        const rows = document.querySelectorAll("#packetTable tbody tr");

        rows.forEach(row => {

            const text = row.innerText.toLowerCase();

            if (text.includes(filter)) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }

        });

    });

}