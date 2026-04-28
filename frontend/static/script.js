/**
 * script.js — Amazon OTDS Frontend Logic
 * Handles search, rendering, keyword highlighting.
 */

// ── DOM refs ─────────────────────────────────────────────────────────────────
const input   = document.getElementById('search-input');
const btn     = document.getElementById('search-btn');
const loading = document.getElementById('loading');
const landing = document.getElementById('landing');
const results = document.getElementById('results');

// ── Events ───────────────────────────────────────────────────────────────────
btn.addEventListener('click', () => doSearch());
input.addEventListener('keydown', e => { if (e.key === 'Enter') doSearch(); });

function runQuery(q) {
    input.value = q;
    doSearch();
}

// ── Search ───────────────────────────────────────────────────────────────────
async function doSearch() {
    const query = input.value.trim();
    if (!query) return;

    landing.style.display = 'none';
    results.style.display = 'none';
    loading.classList.add('active');

    try {
        const resp = await fetch('/api/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query }),
        });

        if (!resp.ok) throw new Error(`Server error (${resp.status})`);

        const data = await resp.json();
        renderResults(data, query);
    } catch (err) {
        results.innerHTML = `<div class="empty-state">
            <div class="empty-icon">⚠️</div>
            <div class="empty-title">Something went wrong</div>
            <div class="empty-sub">${escapeHtml(err.message)}</div>
        </div>`;
        results.style.display = 'block';
    } finally {
        loading.classList.remove('active');
    }
}

// ── Highlight keywords in text ───────────────────────────────────────────────
function highlightKeywords(text, query) {
    if (!query) return escapeHtml(text);
    const safe = escapeHtml(text);
    const words = query.split(/\s+/).filter(w => w.length > 2);
    if (!words.length) return safe;

    const pattern = new RegExp(`(${words.map(escapeRegex).join('|')})`, 'gi');
    return safe.replace(pattern, '<mark>$1</mark>');
}

function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

function escapeRegex(str) {
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// ── Render results ───────────────────────────────────────────────────────────
function renderResults(data, query) {
    const r       = data.results || [];
    const summary = data.summary || [];
    const answer  = data.final_answer || '';
    const meta    = data.metadata || {};

    if (!r.length) {
        results.innerHTML = `<div class="empty-state">
            <div class="empty-icon">🤷</div>
            <div class="empty-title">No results found</div>
            <div class="empty-sub">Try a different query or use one of the suggestions.</div>
        </div>`;
        results.style.display = 'block';
        return;
    }

    let html = '';

    // ── Meta pills
    html += '<div class="meta-bar">';
    (meta.topics || []).forEach(tp => {
        html += `<span class="pill pill-topic">📌 ${escapeHtml(tp)}</span>`;
        const sent = (meta.topic_sentiments || {})[tp] || 'neutral';
        const cls  = sent === 'positive' ? 'pill-positive' : sent === 'negative' ? 'pill-negative' : 'pill-neutral';
        const icon = sent === 'positive' ? '👍' : sent === 'negative' ? '👎' : '➖';
        html += `<span class="pill ${cls}">${icon} ${sent}</span>`;
    });
    html += `<span class="pill pill-count">📊 ${r.length} products</span>`;
    html += '</div>';

    // ── Stats row
    const posCount = r.filter(x => x.sentiment_label === 'positive').length;
    const negCount = r.filter(x => x.sentiment_label === 'negative').length;
    const avgRat   = (r.reduce((s, x) => s + x.rating, 0) / r.length).toFixed(1);
    const starStr  = '★'.repeat(Math.round(avgRat));

    html += `<div class="stats-row">
        <div class="stat-box">
            <div class="stat-val">${r.length}</div>
            <div class="stat-label">Products Found</div>
        </div>
        <div class="stat-box">
            <div class="stat-val" style="color:var(--amz-star)">${starStr} ${avgRat}</div>
            <div class="stat-label">Avg Rating</div>
        </div>
        <div class="stat-box">
            <div class="stat-val" style="color:var(--green)">${posCount}</div>
            <div class="stat-label">Positive</div>
        </div>
        <div class="stat-box">
            <div class="stat-val" style="color:var(--red)">${negCount}</div>
            <div class="stat-label">Negative</div>
        </div>
    </div>`;

    // ── AI Summary
    if (answer) {
        html += `<div class="section-hdr">✨ AI Summary</div>`;
        html += `<div class="answer-box">${escapeHtml(answer)}</div>`;
    }

    // ── Key Insights
    if (summary.length) {
        html += `<div class="section-hdr">📋 Key Insights</div>`;
        summary.forEach(s => {
            html += `<div class="insight-card"><span class="insight-icon">▸</span><span>${escapeHtml(s)}</span></div>`;
        });
    }

    // ── Product cards (top 5)
    const top = r.slice(0, 5);
    html += `<div class="section-hdr">📦 Customer Reviews (${top.length} results)</div>`;

    top.forEach((item, i) => {
        const filled = '★'.repeat(item.rating);
        const empty  = '★'.repeat(5 - item.rating);
        const sentCls = item.sentiment_label === 'positive' ? 'badge-positive'
                      : item.sentiment_label === 'negative' ? 'badge-negative'
                      : 'badge-neutral';
        const sentLabel = item.sentiment_label === 'positive' ? '✓ Positive'
                        : item.sentiment_label === 'negative' ? '✗ Negative'
                        : '~ Mixed';

        html += `<div class="result-card" style="animation:slideUp .4s ease ${0.1 + i * 0.06}s both">
            <div class="result-header">
                <span class="result-name">${escapeHtml(item.product_name)}</span>
                <span class="result-score">Score ${item.score.toFixed(4)}</span>
            </div>
            <div class="stars">
                <span class="star">${filled}</span><span class="star-empty">${empty}</span>
                <span class="rating-label">${item.rating}.0 out of 5</span>
            </div>
            <div class="result-text">${highlightKeywords(item.text, query)}</div>
            <div class="result-footer">
                <span class="badge badge-topic">${escapeHtml(item.topic)}</span>
                <span class="badge ${sentCls}">${sentLabel}</span>
                <span class="badge-pid">${escapeHtml(item.product_id)}</span>
            </div>
        </div>`;
    });

    results.innerHTML = html;
    results.style.display = 'block';
}
