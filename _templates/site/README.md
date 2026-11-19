# 新站点模板

复制本目录的 `index.html` 到 `site/<slug>/index.html`。例如，新入口名为 `notes`：

```sh
mkdir -p site/notes
cp _templates/site/index.html site/notes/index.html
```

替换 `__SLUG__`、`__SITE_TITLE_ZH__`、`__SITE_TITLE_EN__`、`__DESCRIPTION_ZH__`、`__DESCRIPTION_EN__`，并在 `site/index.html` 添加导航卡片。原始模板不在发布目录中。

模板从父目录加载 `../assets/studio.css` 与 `../assets/studio.js`，可以直接使用共用外观和语言切换。单独网站需要更多样式／逻辑时，把文件放在该网站目录内并使用相对路径引用。

内容完善后移除模板里的 `noindex,follow`，并将正式地址添加到 `site/sitemap.xml`。站点目录名使用小写英文字母、数字和连字符。
