// ========== 首页逻辑 ==========

async function initHome() {
  const liveContainer = document.getElementById('live-banner');
  const todayContainer = document.getElementById('today-list');
  const updateTimeEl = document.getElementById('update-time');

  // 骨架屏
  renderSkeleton(liveContainer, 1);
  renderSkeleton(todayContainer, 3);

  // 并行加载数据
  const [liveData, todayData, meta] = await Promise.all([
    loadJSON('live.json'),
    loadJSON('today.json'),
    loadJSON('_meta.json')
  ]);

  // 更新时间
  if (meta && meta.last_updated) {
    updateTimeEl.textContent = `数据更新于 ${timeAgo(meta.last_updated)}`;
  }

  // 正在比赛置顶
  if (liveData && liveData.matches && liveData.matches.length > 0) {
    const first = liveData.matches[0];
    liveContainer.innerHTML = `
      <div class="live-banner">
        <div class="match-header">
          <span class="status-badge live">🟢 进行中</span>
          <span>${first.event_name}</span>
          <span>${first.round}</span>
        </div>
        <div class="score-row">
          <span class="player-name">${first.player1?.name || ''}</span>
          <span class="score-num">${first.player1?.score ?? '-'}</span>
        </div>
        <div class="score-row">
          <span class="player-name">${first.player2?.name || ''}</span>
          <span class="score-num">${first.player2?.score ?? '-'}</span>
        </div>
        <div class="match-footer">
          ${first.best_of ? `<span>BO${first.best_of}</span>` : ''}
          ${first.highest_break ? `<span>单杆最高 ${first.highest_break}</span>` : ''}
        </div>
      </div>
    `;
  } else {
    liveContainer.innerHTML = `
      <div class="match-card" style="text-align:center; color:#999; padding:32px;">
        当前没有正在进行的比赛
      </div>
    `;
  }

  // 今日赛程
  if (todayData && todayData.matches) {
    todayContainer.innerHTML = todayData.matches.map(matchCardHTML).join('');
  } else {
    todayContainer.innerHTML = `
      <div class="match-card" style="text-align:center; color:#999;">
        今日暂无赛程数据
      </div>
    `;
  }
}

document.addEventListener('DOMContentLoaded', initHome);
