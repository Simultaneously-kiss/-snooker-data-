// ========== 赛程签表页逻辑 ==========

async function initSchedule() {
  const listContainer = document.getElementById('schedule-list');

  renderSkeleton(listContainer, 5);

  const todayData = await loadJSON('today.json');

  if (todayData && todayData.matches) {
    listContainer.innerHTML = todayData.matches.map(matchCardHTML).join('');
  } else {
    listContainer.innerHTML = `
      <div class="match-card" style="text-align:center; color:#999;">
        暂无赛程数据
      </div>
    `;
  }
}

document.addEventListener('DOMContentLoaded', initSchedule);
