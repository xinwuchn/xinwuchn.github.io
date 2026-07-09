# 主页维护指南

本站基于 [al-folio](https://github.com/alshedivat/al-folio) Jekyll 模板构建，通过 Docker 本地预览、GitHub Actions 自动部署到 `xinwuchn.github.io`。

---

## 目录

1. [快速启动本地预览](#1-快速启动本地预览)
2. [常见更新操作](#2-常见更新操作)
3. [项目文件结构说明](#3-项目文件结构说明)
4. [发布到线上](#4-发布到线上)
5. [常见问题](#5-常见问题)

---

## 1. 快速启动本地预览

需要一个 Docker daemon。本机用 **OrbStack**（比 Docker Desktop 省内存、启动快）：

```bash
open -a OrbStack            # 启动，等菜单栏图标就绪
docker context use orbstack # 一次性设置，之后持久生效
```

> OrbStack 设置 → General 勾选 "Start at login" 可省掉第一步。
> 想换回 Docker Desktop：`docker context use desktop-linux`（注意两者镜像存储独立，切换后需重新构建）。

### 方式一：VSCode Container Tools 扩展（推荐）

装扩展 `ms-azuretools.vscode-containers`，然后：

1. 右键 `compose.yaml` → **Compose Up**（首次会自动构建镜像）
2. 浏览器访问 <http://localhost:8080>
3. 收工：侧边栏鲸鱼图标 → Containers → 右键容器 → **Compose Down**

侧边栏里右键容器还能 `View Logs` 看 Jekyll 构建输出和报错，`Attach Shell` 进容器调试。

> 不要用镜像上的 `Run` / `Run Interactive`——它不带端口映射和目录挂载，容器起来了也访问不到。只有 Compose Up 才会读 `compose.yaml` 里的完整参数。

### 方式二：命令行

```bash
docker compose up          # 首次自动构建；Ctrl-C 停止
docker compose up -d --build   # 改了 Dockerfile / Gemfile 后强制重建
```

### 热重载行为

- **源文件改动**（`_pages/`、`_posts/`、`_data/` 等）自动触发增量重建，浏览器**自动刷新**（livereload 走 35729 端口，已在 `compose.yaml` 里映射）
- **`_config.yml` 改动**也会自动重启 Jekyll——`bin/entry_point.sh` 里有个 `inotifywait` 循环盯着它。重启约需十几秒，看容器日志确认
- 极少数情况下 watcher 漏事件，`touch` 任一 `_pages/*.md` 强制重建，或 Compose Down 再 Up

---

## 2. 常见更新操作

### 2.1 修改个人信息（关于页）

- 文件：`_pages/about.md`
- 头像图片：`assets/img/Imagephoto.jpg`（frontmatter 的 `profile.image`）
- subtitle、职位等写在 frontmatter 里，正文用 HTML/Markdown 自由编辑

### 2.2 添加 News（主页滚动公告）

- 目录：`_news/`
- 新建文件 `announcement_N.md`：
  ```yaml
  ---
  layout: post
  date: 2025-06-01
  inline: true
  related_posts: false
  ---
  One-line news content here. :sparkles:
  ```
- 显示数量在 `_config.yml` 的 `announcements.limit` 控制

### 2.3 添加 / 更新论文

- 文件：`_bibliography/papers.bib`（标准 BibTeX 格式）
- `selected={true}` 的条目会显示在首页 "Selected Publications"
- 可选字段（al-folio 扩展）：
  - `abbr`：期刊缩写徽章（左侧显示）
  - `abstract`：展开按钮
  - `pdf`：PDF 文件名（放 `assets/pdf/`）或 URL
  - `preview`：缩略图（放 `assets/img/publication_preview/`）
  - `html`：论文网页
  - `bibtex_show={true}`：显示 BibTeX 按钮
  - `selected={true}`：标记为 selected paper

### 2.4 添加会议报告（Presentations 页）

- **数据文件**：`_data/presentations.yml`
- **渲染模板**：`_pages/teaching.md`（即 `/presentations/` 页面）
- 直接在 YAML 里追加条目即可（**最新的放最上面**）：
  ```yaml
  - type: invited          # invited | contributed | poster
    title: "Talk title"
    conference: "Conference full name"
    location: "City, Country"
    date: 2025-06-15       # YYYY-MM-DD
    year: 2025             # 用于分组
    lat: 35.6762           # 可选，用于世界地图标记
    lng: 139.6503          # 可选，配合 lat 一起写
    url: https://...       # 可选，会议官网（会议名称变超链接）
    slides: /assets/pdf/talks/xxx.pdf  # 可选
    authors: "Xin Wu, Collaborator"    # 可选，"Xin Wu" 自动加下划线
    abstract: "One-line summary."      # 可选
  ```
- **Invited 报告会被加红色竖条和浅红背景加强显示**
- 页面顶部有一张 **世界地图**，按 `lat`/`lng` 显示参会位置，按类型着色。坐标可从 [latlong.net](https://www.latlong.net/) 或 Google Maps 右键获取
- Slides PDF 放 `assets/pdf/talks/`（按需 `mkdir`）

### 2.5 写博客

- 目录：`_posts/`
- 文件名格式：`YYYY-MM-DD-slug.md`
- Frontmatter 示例：
  ```yaml
  ---
  layout: post
  title: 你的标题
  date: 2025-06-01
  description: 一句话摘要
  tags: [MD, DFT]          # 显示在 Blog 首页的标签
  categories: Research     # 显示分类
  ---
  ```
- `_posts/to-post-list.md` 是待写文章清单（个人备忘，不会发布）

### 2.6 更新 CV

- 模式一：**通过 YAML 数据文件**（推荐）
  - 编辑 `assets/json/resume.json`，页面会自动渲染
- 模式二：**直接 PDF**
  - 把 PDF 放 `assets/pdf/my_cv.pdf`，在 `_pages/cv.md` frontmatter 设 `cv_pdf: my_cv.pdf`

### 2.7 更改导航栏顺序或隐藏页面

- 编辑各 `_pages/*.md` 的 frontmatter：
  - `nav: true` / `false` 控制是否显示
  - `nav_order: N` 控制顺序
- 当前导航（`nav: true`）：About(1) → Publications(2) → Presentations(3) → CV(4) → Blog(5)

### 2.8 开关站点功能

编辑 `_config.yml` 后容器会**自动重启 Jekyll**，等十几秒生效。常用开关：

| 选项 | 作用 |
|---|---|
| `enable_darkmode` | 暗黑模式切换 |
| `enable_math` | MathJax 数学公式 |
| `enable_medium_zoom` | 图片放大查看 |
| `enable_publication_badges.google_scholar` | Google Scholar 引用徽章（容易限流，已关闭）|
| `giscus_comments`（在 defaults 里）| 所有页面底部的评论区 |
| `giscus.reactions_enabled` | 评论区顶部 emoji 反应 |
| `search_enabled` | 顶部搜索框 |

---

## 3. 项目文件结构说明

### 根目录

| 文件 / 目录 | 作用 | 你需要动吗？ |
|---|---|---|
| `_config.yml` | **站点全局配置**：标题、作者信息、导航、插件开关、Giscus、社交链接、Scholar ID 等 | 偶尔改 |
| `Dockerfile` | Docker 镜像构建定义（Ruby + Jekyll + ImageMagick） | 基本不动 |
| `compose.yaml` | 本地预览的容器编排（端口映射 + 目录挂载） | 基本不动 |
| `Gemfile` / `Gemfile.lock` | Ruby 依赖声明和锁定版本 | 加插件时改 |
| `package.json` / `package-lock.json` | 少量 npm 工具（purgecss 等） | 基本不动 |
| `purgecss.config.js` | 生产构建时清理无用 CSS 的配置 | 基本不动 |
| `robots.txt` | 搜索引擎爬虫规则 | 基本不动 |
| `LICENSE` | MIT 许可证 | 不动 |
| `README.md` | 仓库 README | 按需 |
| `MAINTENANCE.md` | **本文件** | — |
| `.github/workflows/deploy.yml` | GitHub Actions 自动部署工作流 | 基本不动 |
| `.dockerignore` / `.gitignore` | 构建和版本控制忽略规则 | 基本不动 |
| `bin/entry_point.sh` | Docker 容器入口脚本，启动 Jekyll serve | 基本不动 |

### 内容目录（**这些才是你经常要改的**）

| 目录 | 作用 |
|---|---|
| `_pages/` | 各独立页面（about / publications / teaching / cv / blog / news / 404） |
| `_posts/` | 博客文章（文件名必须 `YYYY-MM-DD-*.md`）|
| `_news/` | 主页滚动的 news/announcements |
| `_bibliography/papers.bib` | 论文数据（BibTeX）|
| `_data/` | YAML 数据文件，见下 |
| `assets/` | 所有静态资源，见下 |

### `_data/` — 结构化数据

| 文件 | 作用 |
|---|---|
| `coauthors.yml` | 合作者信息，papers.bib 里引用名会自动链接 |
| `cv.yml` | CV 页面的结构化数据（如果 cv.md 用数据模式）|
| `venues.yml` | 期刊/会议的全名到缩写映射（显示 abbr 徽章）|
| `presentations.yml` | **会议报告数据**（你主要更新的文件之一）|

### `assets/` — 静态资源

| 子目录 | 作用 |
|---|---|
| `img/` | 图片（头像、封面、博客插图）|
| `img/publication_preview/` | 论文缩略图 |
| `pdf/` | 可下载 PDF（论文、CV、slides）|
| `pdf/talks/` | 会议报告 slides |
| `bibliography/` | bib 文件的额外资源（al-folio 内部）|
| `css/` | 自定义 CSS（极少需要改）|
| `js/` | 自定义 JavaScript |
| `fonts/` / `webfonts/` | 字体 |
| `json/` / `plotly/` / `jupyter/` / `audio/` / `video/` / `html/` | 嵌入到博客/页面的多媒体素材 |

### 模板和插件（**一般不需要改**）

| 目录 | 作用 |
|---|---|
| `_layouts/*.liquid` | 页面布局模板（default / page / post / about / bib / cv / distill / page 等）|
| `_includes/*.liquid` | 可复用的模板片段（header、footer、figure、giscus、news 等）|
| `_sass/` | SCSS 样式源文件（主题、变量、响应式等）|
| `_plugins/*.rb` | 自定义 Jekyll 插件（引用数抓取、文件存在检查、下载第三方库等）|

### 生成产物和缓存（**勿手动修改**）

| 目录 | 作用 |
|---|---|
| `_site/` | Jekyll 构建输出（本地预览用），已 gitignore |
| `.jekyll-cache/` | 增量构建缓存，已 gitignore |
| `node_modules/` | npm 依赖，已 gitignore |

---

## 4. 发布到线上

`.github/workflows/deploy.yml` 会在你 `git push` 到 `master` 分支时自动构建并部署到 GitHub Pages。

常规流程：

```bash
# 本地预览确认无误后
git add .
git commit -m "update: ..."
git push origin master
```

几分钟后 <https://xinwuchn.github.io> 自动刷新。在 GitHub 仓库的 Actions 标签页可查看部署进度。

---

## 5. 常见问题

### Q: 改了 `_data/presentations.yml` 页面没更新？

Docker on macOS 的文件监听偶尔漏事件。解决：
```bash
touch _pages/teaching.md
```
或直接重启容器。

### Q: 改了 `_config.yml` 没效果？

正常情况下 `bin/entry_point.sh` 会检测到并自动重启 Jekyll，等十几秒即可。先看日志确认：
```bash
docker compose logs -f site   # 应出现 "Change detected to _config.yml, restarting Jekyll"
```
没出现就手动重启：
```bash
docker compose restart site
```

### Q: 构建报 `Could not locate the included file 'xxx.md'`？

某个 layout 引用了不存在的文件。通常是模板示例页面遗留，检查对应 `_pages/*.md` 和 `_layouts/*.liquid`。

### Q: Google Scholar 报 429 Too Many Requests？

被 Scholar 限流了。本站已关闭自动抓取引用数（`_config.yml` 里 `enable_publication_badges.google_scholar: false`）。如需开启自行评估风险。

### Q: 首次构建很慢？

分两层：

- **镜像构建**（装 Ruby gems 和 ImageMagick）首次几分钟，之后走 Docker 层缓存，除非改了 `Dockerfile` / `Gemfile`
- **Jekyll 站点构建**首次要生成所有响应式图片，约 100 秒。之后有 `.jekyll-cache/` 缓存，一般 7–10 秒

`_site/` 和 `.jekyll-cache/` 挂载在宿主机上，Compose Down 也不会丢，所以重开容器通常十几秒就能访问。

### Q: 想添加新的顶层页面？

1. 在 `_pages/` 新建 `yourpage.md`
2. frontmatter 设置：
   ```yaml
   ---
   layout: page
   permalink: /yourpage/
   title: Your Page
   nav: true
   nav_order: 6
   ---
   ```
3. 正文用 Markdown + Liquid 编写

---

_最后更新：2026-07-09_
