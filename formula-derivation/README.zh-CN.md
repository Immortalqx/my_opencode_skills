# formula-derivation

[English](./README.md) | 中文

`formula-derivation` 用于把松散的研究理论笔记整理成一条连贯的推导线。它适合构建和组织公式，不是用于审查已经定稿的 theorem-proof 包。

当你需要澄清假设、定义正确对象、区分恒等式和近似、或写出可放进论文的推导骨架时，可以使用 `formula-derivation` skill：

```text
使用 formula-derivation skill 把这些笔记整理成论文风格的推导。
```

## 依赖说明

不需要 API key。

## 工作流程

1. 固定要解释的现象和要支持的 claim。
2. 选择贯穿整个推导的不变量或核心对象。
3. 先写清假设和符号。
4. 把每一步分类为恒等式、命题、近似或解释。
5. 输出内部推导笔记、论文风格理论草稿，或 blocker report。

## 内容

- `formula-derivation/SKILL.md`：Claude skill 定义。
- 外层 `README.md` 和 `README.zh-CN.md` 只是仓库说明，不会被安装到 Claude skills 目录。

## 安装

```bash
cp -r formula-derivation/formula-derivation/* ~/.claude/skills/formula-derivation/
```

之后就可以用 `/formula-derivation` 调用。
