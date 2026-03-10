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
* **直接引用**：支持通过 GitHub Raw 链接直接导入 Sing-box 客户端。

## 🚀 使用方法

在你的 Sing-box 配置文件中的 `route.rule_set` 部分，参考以下格式添加规则：

```json
{
  "tag": "skk-rules",
  "type": "remote",
  "format": "binary",
  "url": "https://raw.githubusercontent.com/KiydreL/sing-box_rulesets/main/rules/此处替换为具体文件名.srs Or https://testingcf.jsdelivr.net/gh/KiydreL/sing-box_rulesets/main/rules/此处替换为具体文件名.srs",
  "download_detour": "proxy"
}
