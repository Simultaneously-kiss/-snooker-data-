// ========== 排名页逻辑 ==========

async function initRanking() {
  const tableBody = document.getElementById('ranking-body');
  const updateTimeEl = document.getElementById('ranking-update');

  tableBody.innerHTML = '<tr><td colspan="6" style="text-align:center; color:#999; padding:32px;">加载中...</td></tr>';

  const data = await loadJSON('rankings-main.json');

  if (data && data.entries && data.entries.length > 0) {
    updateTimeEl.textContent = `数据更新于 ${timeAgo(data.updated_at)}`;

    tableBody.innerHTML = data.entries.map(entry => {
      const change = entry.rank - (entry.previous_rank || entry.rank);
      let changeHTML = '<span class="rank-change same">—</span>';
      if (change < 0) changeHTML = `<span class="rank-change up">↑ ${Math.abs(change)}</span>`;
      else if (change > 0) changeHTML = `<span class="rank-change down">↓ ${change}</span>`;

      return `
        <tr>
          <td class="rank-num">${entry.rank}</td>
          <td><strong>${entry.name}</strong></td>
          <td>${entry.nationality || '-'}</td>
          <td>£${(entry.points || 0).toLocaleString()}</td>
          <td>${changeHTML}</td>
          <td>${entry.tournaments_played || '-'}</td>
        </tr>
      `;
    }).join('');
  } else {
    tableBody.innerHTML = '<tr><td colspan="6" style="text-align:center; color:#999; padding:32px;">暂无排名数据</td></tr>';
  }
}

document.addEventListener('DOMContentLoaded', initRanking);
