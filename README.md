# WACS - Webpage Automatic Checking System
### An automatic checking, scoring system for web-page.

 

<br>

## Environments
- Python 3.7.5
- MySQL


## Setting

### setting.ini
- db: your database connection, user, password, schema-name
- manual: decide which homework you want to score
- save: the directory path saving html, screenshot, google-speed-api json file
- status_filt: filt the status of db record

### wacs_ult/reduct.ini
- set the weight of each check-item

 

<br>

 

## Check Item
- Check if the page file is not existed or is empty or status-code: 404 --- 1 --- `vital_check.py`

- Check if \<!DOCTYPE\> is HTML --- 2 --- `do_doc_type_check()`

- Check if charset is UTF-8 --- 3 --- `do_charset_check()`

- Check if lang is zh_TW --- 4 --- `do_lang_check()`

- Check if title is empty --- 5 --- `do_title_check()`

- Check if content is all in \<body- --- 7 --- `do_head_body_check()`


- Check if page has horizontal scroll-bar --- 8 --- `check_scroll_bar`

- Check if the speed of page-loading is too slow --- 9 --- `gps_helper.py`

- Check if the image is failed to display --- 10 --- `do_img_display_check()`


- Check if file name of the page HTML file contains bad character --- 11 --- `do_page_name_check()`

- Check if all upload src name contains bad character --- 12、13、15 --- `do_all_src_name_check()`

- Check if a new window will open when accessing external-domain page --- 14 --- `do_window_open_check()`


- Check if css is in the correct folder --- 16 --- `do_css_check()`

- Check if JavaScript is in the correct folder --- 17 --- `do_js_check()`


- Check if the setting of image is wrong --- 18、19 --- `do_img_setting_check()`

- Check if the blank space of attribute is wrong --- 22 --- `check_attr_space`

- Check if the usage of \<ul\> is wrong --- 24 --- `do_ul_tag_check()`

- Check if the usage of \<ol\> is wrong --- 25 --- `do_ol_tag_check()`

- Check if the usage of \<li\> is wrong --- 26 --- `do_li_tag_check()` 

<br>

## Unstable Check-item

- Check if the start tag and the end tag of elements  is wrong --- 20 --- `do_tags_check()`

- Check if the count of `<` and `>` is wrong --- 21 --- `do_gl_symbols_check()`

- Check if the `"` sybols is wrong --- 23 --- `do_attr_quote_check()`
