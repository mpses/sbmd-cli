# sbmd-cli

Scrapbox (Cosense) ↔ Obsidian Markdown Converter

## 概要

Obsidian スタイルの Markdown と Scrapbox (Cosense) のマークアップを相互変換する Python スクリプトです。macOSのクリップボードを使って簡単に変換できます。

\* This file is automatically generated by Claude 4. 

## 機能

### 1. Markdown → Scrapbox (`md_to_sb.py`)
Obsidian の Markdown を Scrapbox マークアップに変換

**対応要素:**
- **数式**: `$formula$` → `[$ formula ]`
- **外部リンク**: `[label](url)` → `[url label]`
- **内部リンク**: `[[Page]]` → `[Page]`
- **太字**: `**text**` → `[* text]`
- **斜体**: `*text*` → `[/ text]`
- **打ち消し線**: `~~text~~` → `[- text]`
- **見出し**: `# Heading` → `[**** Heading]`
- **リスト**: `- item` → `item`
- **引用**: `> quote` → `> quote`
- **コードブロック**: ````code```` → `code:lang`

### 2. Scrapbox → Markdown (`sb_to_md.py`)
Scrapbox マークアップを Obsidian の Markdown に変換

**対応要素:**
- **数式**: `[$ formula ]` → `$formula$`
- **太字**: `[* text]` や `[[text]]` → `**text**`
- **斜体**: `[/ text]` → `*text*`
- **打ち消し線**: `[- text]` → `~~text~~`
- **外部リンク**: `[url label]` → `[label](url)`
- **内部リンク**: `[Page]` → `[[Page]]`
- **見出し**: `[*** Heading]` → `## Heading`
- **リスト**: 自動的に `- ` プレフィックス追加
- **引用**: `> quote` → `> quote`
- **コードブロック**: `code:lang` → ````lang````

## 使い方

### 前提条件
- macOS
- Python 3.6+

### Markdown → Scrapbox
```bash
# 1. Markdown テキストをコピー (Cmd+C)
# 2. スクリプト実行
$ python3 src/md_to_sb.py
# 3. Scrapbox にペースト (Cmd+V)
```

### Scrapbox → Markdown
```bash
# 1. Scrapbox のテキストをコピー (Cmd+C)
# 2. スクリプト実行
$ python3 src/sb_to_md.py
# 3. Obsidian などにペースト (Cmd+V)
```

## インストール

```bash
$ git clone <this repo>
$ cd sbmd-cli
# お好みで ~/bin などパスを通したフォルダに移動 
$ chmod +x md_to_sb.py sb_to_md.py
```

## 例

### Markdown → Scrapbox
**入力 (Markdown):**
```markdown
# タイトル
**太字** と *斜体* と ~~打ち消し~~
[Obsidian](https://obsidian.md) と [[内部リンク]]
$E = mc^2$
```

**出力 (Scrapbox):**
```
[**** タイトル]
[* 太字] と [/ 斜体] と [- 打ち消し]
[https://obsidian.md Obsidian] と [内部リンク]
[$ E = mc^2 ]
```

### Scrapbox → Markdown
**入力 (Scrapbox):**
```
[*** 見出し]
[* 強調] テキスト
[https://example.com サイト]
[$ \sum_{i=1}^n i ]
```

**出力 (Markdown):**
```markdown
## 見出し
- **強調** テキスト
- [サイト](https://example.com)
- $\sum_{i=1}^n i$
```