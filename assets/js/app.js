// ========== 公共工具函数 ==========

const API_BASE = './data/';

/**
 * 加载 JSON 数据
 */
async function loadJSON(filename) {
  try {
    const res = await fetch(`${API_BASE}${filename}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (e) {
    console.error(`加载 ${filename} 失败:`, e);
    return null;
  }
}

/**
 * 渲染骨架屏
 */
function renderSkeleton(container, count = 3) {
  let html = '';
  for (let i = 0; i < count; i++) {
    html += `
      <div class="skeleton">
        <div class="skeleton-line short"></div>
        <div class="skeleton-line medium"></div>
        <div class="skeleton-line short"></div>
      </div>
    `;
  }
  container.innerHTML = html;
}

/**
 * 格式化时间显示
 */
function timeAgo(isoString) {
  if (!isoString) return '';
  const now = new Date();
  const time = new Date(isoString);
  const diff = Math.floor((now - time) / 1000);

  if (diff < 60) return '刚刚';
  if (diff < 3600) return `${Math.floor(diff / 60)} 分钟前`;
  if (diff < 86400) return `${Math.floor(diff / 3600)} 小时前`;
  return `${Math.floor(diff / 86400)} 天前`;
}

/**
 * 渲染比赛卡片 HTML
 */
function matchCardHTML(match) {
  const p1 = match.player1 || {};
  const p2 = match.player2 || {};
  const statusText = {
    live: '进行中',
    upcoming: '即将开赛',
    completed: '已结束'
  }[match.status] || match.status;

  const tierClass = match.event_tier || 'ranking';

  return `
    <div class="match-card ${match.status === 'live' ? 'live' : ''}">
      <div class="match-header">
        <span class="status-badge ${match.status}">${statusText}</span>
        <span class="event-tag ${tierClass}">${match.event_name || ''}</span>
        <span>${match.round || ''}</span>
      </div>
      <div class="score-row">
        <span class="player-name ${p1.score != null && p2.score != null && p1.score > p2.score ? 'winner' : ''}">
          ${p1.name || 'TBD'}
        </span>
        <span class="score-num ${p1.score != null && p2.score != null && p1.score > p2.score ? 'winner' : ''}">
          ${p1.score != null ? p1.score : '-'}
        </span>
      </div>
      <div class="score-row">
        <span class="player-name ${p1.score != null && p2.score != null && p2.score > p1.score ? 'winner' : ''}">
          ${p2.name || 'TBD'}
        </span>
        <span class="score-num ${p2.score != null && p1.score != null && p2.score > p1.score ? 'winner' : ''}">
          ${p2.score != null ? p2.score : '-'}
        </span>
      </div>
      <div class="match-footer">
        ${match.best_of ? `<span>BO${match.best_of}</span>` : ''}
        ${match.highest_break ? `<span>单杆最高 ${match.highest_break}</span>` : ''}
        ${match.scheduled_at ? `<span>${match.scheduled_at}</span>` : ''}
      </div>
    </div>
  `;
}
