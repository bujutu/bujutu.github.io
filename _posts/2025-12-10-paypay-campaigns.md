---
title: "PayPay × 自治体キャンペーン（自動更新）"
layout: post
date: 2025-12-11 04:50:53
description: "PayPayと自治体のポイント還元キャンペーン一覧（自動更新）。"
tags: [paypay, 自治体, キャンペーン, 自動更新]
---

> 最終更新: **2025-12-11 04:50:53**

PayPay × 自治体 の還元キャンペーン情報を自動収集し、一覧化しています。  
高還元キャンペーンはすぐ終わることがあるため、最新情報は必ず公式ページもご確認ください。


{% include toc.html %}


---


{% if campaigns | length == 0 %}
現在取得できるキャンペーンはありません。
{% else %}

# 開催中

{% assign now_list = campaigns | where: "status", "開催中" %}

{% if now_list.size == 0 %}
現在「開催中」のキャンペーンはありません。
{% else %}
{% for item in now_list %}
## {{ item.name }}

- **状態**: {{ item.status }}
- **期間**: {{ item.period }}
- **還元率**: {{ item.rate }}
- **公式ページ**: [リンク]({{ item.url }})

---
{% endfor %}
{% endif %}

# 開催予定

{% assign upcoming_list = campaigns | where: "status", "開催予定" %}

{% if upcoming_list.size == 0 %}
現在「開催予定」のキャンペーンはありません。
{% else %}
{% for item in upcoming_list %}
## {{ item.name }}

- **状態**: {{ item.status }}
- **期間**: {{ item.period }}
- **還元率**: {{ item.rate }}
- **公式ページ**: [リンク]({{ item.url }})

---
{% endfor %}
{% endif %}

{% endif %}


※本記事は自動生成されています。