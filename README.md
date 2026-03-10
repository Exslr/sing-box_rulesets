# Sing-box 规则集自动更新 (基于 SKK.moe)

<p align="center">
  <img src="https://img.shields.io/github/actions/workflow/status/KiydreL/sing-box_rulesets/auto-update.yml?style=flat-square&label=自动更新状态" alt="Update Status">
  <img src="https://img.shields.io/github/v/release/KiydreL/sing-box_rulesets?style=flat-square&color=orange&label=最新版本" alt="Release">
  <img src="https://img.shields.io/badge/格式-二进制%20(.srs)-blue?style=flat-square" alt="Format">
</p>

## 📖 项目简介

本项目是一个自动化工具，旨在为 **Sing-box** 用户提供高性能、实时更新的规则集。

通过 GitHub Actions，本项目每周会自动抓取 [SKK.moe (SukkaW/Surge)](https://github.com/SukkaW/Surge) 的最新规则，并将其转换为 Sing-box 专用的 **二进制规则集 (.srs)** 格式。

## ✨ 项目特性

* **自动同步**：每周定期运行脚本，确保规则始终处于最新状态。
* **二进制格式**：预编译的 `.srs` 文件，相比 JSON 格式加载速度更快、内存占用更低。
* **多样化获取**：
    * **在线引用**：支持通过 GitHub Raw 链接直接导入。
    * **打包下载**：在 [Releases](https://github.com/KiydreL/sing-box_rulesets/releases) 页面提供全量规则的 ZIP 压缩包，方便批量部署或本地使用。

## 🚀 使用方法

### 1. 在线远程引用
在 Sing-box 配置的 `route.rule_set` 部分添加：

```json
{
  "tag": "skk-rules",
  "type": "remote",
  "format": "binary",
  "url": "[https://raw.githubusercontent.com/KiydreL/sing-box_rulesets/main/rules/此处替换为具体文件名.srs](https://raw.githubusercontent.com/KiydreL/sing-box_rulesets/main/rules/此处替换为具体文件名.srs)",
  "download_detour": "proxy"
}
```

### 2. 离线/本地使用

如果你不想通过远程链接加载，可以手动下载规则包：

1.  前往 [Releases 页面](https://github.com/KiydreL/sing-box_rulesets/releases) 下载最新的规则压缩包（例如 `rules.zip`）。
2.  解压后将所需的 `.srs` 文件放入 Sing-box 程序所在的目录或指定的 `rules` 文件夹中。
3.  在配置文件中按以下格式引用本地文件：

```json
{
  "tag": "local-skk-rules",
  "type": "local",
  "format": "binary",
  "path": "rules/此处替换为解压后的文件名.srs"
}
```

---

```markdown
## 🤝 鸣谢

本项目离不开以下优秀项目和开发者的支持：

* **规则原始来源**：[SukkaW/Surge](https://github.com/SukkaW/Surge) (即 [SKK.moe](https://skk.moe/)) —— 提供了高质量且持续更新的原始分流规则。
* **核心转换工具**：[Sing-box](https://github.com/SagerNet/sing-box) —— 提供了强大的二进制规则转换与运行环境。
* **自动化平台**：[GitHub Actions](https://github.com/features/actions) —— 实现了规则的自动化更新与发布。
