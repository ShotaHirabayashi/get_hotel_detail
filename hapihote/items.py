# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HapihoteItem(scrapy.Item):
# head info
    B_hotel_name = scrapy.Field()
    C_address = scrapy.Field()
    D_tel = scrapy.Field()

    G_head_title = scrapy.Field()
    F_hapi_url = scrapy.Field()
    H_hotel_name_kana = scrapy.Field()
    J_img_url = scrapy.Field()
    K_discribe = scrapy.Field()

    V_map_code = scrapy.Field()

#th
    # th_facility = scrapy.Field()
    # th_member_service = scrapy.Field()
    # th_room_service = scrapy.Field()
    # th_other_service = scrapy.Field()
    # th_payment = scrapy.Field()
    # th_outside = scrapy.Field()
    # th_how_many = scrapy.Field()
    # th_reservation = scrapy.Field()
    # th_offial_site = scrapy.Field()
    # th_twitter = scrapy.Field()
    # th_hotel_group = scrapy.Field()
    #content > div.guide.bottom > div > a.pagerNext
    # 1 132 222 1361


    # #last_num = len(response.css(".guide.bottom > .pagerNav").css('a'))
    # #  response.css(".guide.bottom > .pagerNav").css('a')[last_num-1].get()
    # response.css(".guide.bottom > .pagerNav").css('a')[3]css('::attr(href)').extract_first()
    # # &gt;&gt;
    # # >>



#td
    M_td_park = scrapy.Field()
    N_td_construct = scrapy.Field()
    L_td_access = scrapy.Field()
    I_td_room_num = scrapy.Field()
    O_td_facility = scrapy.Field()
    S_td_room_service = scrapy.Field()
    T_td_other_service = scrapy.Field()
    W_td_payment = scrapy.Field()
    U_td_outside = scrapy.Field()
    Q_td_how_many = scrapy.Field()
    X_td_reservation = scrapy.Field()
    E_td_offcial_site = scrapy.Field()
    P_td_hotel_group = scrapy.Field()
    R_td_member_service = scrapy.Field()
#料金設定

    Y_td_payment_setting = scrapy.Field()

    pass


# 設備
# メンバー特典
# ルームサービス
# その他サービス
# 支払い/クレジットカード
# 外出
# 利用人数
# 予約
# オフィシャルサイト
# Twitter
# ホテルグループ

#料金設定


####################
    #head
# headのtitle
# ホテルのハピホテ URL
# ホテル名
# ホテル名(カタカナ))
# 画像URL
# ホテル説明
# 住所
# 電話番号
# マップコード