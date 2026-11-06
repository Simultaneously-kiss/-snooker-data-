# 斯诺克赛事数据（非官方球迷工具）

纯静态数据网站，展示 WST 公开赛事信息：正在比赛、赛程签表、世界排名。
数据每小时自动从 [wst.tv](https://wst.tv) 公开页面抓取一次，存为静态 JSON，由 GitHub Pages 托管。

## 这是什么

- ❌ 不是官方应用，不提供直播、视频、回放
- ✅ 是给斯诺克球迷用的免费数据查询工具
- ✅ 所有数据来自公开网页整理，客观事实展示

## 技术栈

- 前端：原生 HTML + Tailwind CSS + 原生 JavaScript
- 爬虫：Python + httpx + selectolax
- 托管：GitHub Pages + GitHub Actions（全自动）

## 本地开发

```bash
# 爬虫测试
cd crawler
pip install -r requirements.txt
python main.py

# 前端直接打开 index.html 即可（需要用本地服务器，因为要 fetch JSON）
# 推荐：npx serve .
```

## 数据更新

GitHub Actions 每小时自动跑一次爬虫，抓取 wst.tv 最新数据并 commit 到 `data/` 目录。
GitHub Pages 自动部署，无需手动操作。

## 免责声明

本项目为斯诺克爱好者自发制作的非官方数据工具。
所有赛事数据、商标、版权均归 WST（World Snooker Tour）所有。
本项目不持有任何赛事版权，不提供直播、视频回放服务。
如需观赛，请前往 WST 官方授权平台。

## License

MIT
