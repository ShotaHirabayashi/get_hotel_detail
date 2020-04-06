# -*- coding: utf-8 -*-
import scrapy
from hapihote.items import HapihoteItem
import logging
import traceback

class HotelSpider(scrapy.Spider):
    name = 'hotel'
    allowed_domains = ['happyhotel.jp']
    start_urls = ['https://happyhotel.jp/searchArea.act']

    def parse(self, response):
        for url in response.css("a::attr('href')").re(r'\?pref_id=\d*'):
            yield response.follow(url,self.parse_topics)

    def parse_topics(self,response):
        for url in response.css("a::attr('href')").re(r'\?jis_code=\d*'):
            yield response.follow(url,self.parse_indivi)

    def parse_indivi(self,response):
        for url in response.css("a::attr('href')").re(r'detail/detail_top.jsp\?id=\d*'):
            yield response.follow(url,self.parse_hotel)

        last_num = (len(response.css(".guide.bottom > .pagerNav").css('a'))-1)
        if response.css(".guide.bottom > .pagerNav").css('a').get() is not None:
            if response.css(".guide.bottom > .pagerNav").css('a')[last_num].xpath('string()').get() ==  '>>':
                print("================================")
                next_page = response.css(".guide.bottom > .pagerNav").css('a')[last_num].css('::attr(href)').extract_first()
                next_page = "https://happyhotel.jp/" + next_page
                print(next_page)
                print("================================")
                print("================================")
                print("================================")
                print("================================")
                yield scrapy.Request(next_page, callback=self.parse_indivi)

    def parse_hotel(self,response):
        try:
            # ホテルページでない場合
            if response.xpath('//*[@id="mainBlock"]/div[1]/div[1]/div/div/h2/img/@alt').get()  == '都道府県を選択する':
                print(response.xpath('//*[@id="mainBlock"]/div[1]/div[1]/div/div/h2/img/@alt').get())
                print("no hotel")
                return


            item =HapihoteItem()

            # ###################
            # header infomation #
            #####################
            # headのtitle
            item["G_head_title"] = response.css('head >title').xpath('string()').get()
            # ホテルのハピホテ URL
            item["F_hapi_url"] = response.url
            # ホテル名
            item["B_hotel_name"] = response.xpath('//*[@id="cHeader"]/h1').xpath('string()').get()
            # ホテル名(カタカナ))
            item["H_hotel_name_kana"] = response.css('head >title::text')[0].re(r'（.*?）') [0].replace("（","").replace("）","")
            #画像URL
            if len(response.xpath('//*[@id="imgCanvasChanger"]/div[1]/img/@src').extract()) == 0:
                print("no image")
                item["J_img_url"] = ""
            else:
                imgxpath = response.xpath('//*[@id="imgCanvasChanger"]/div[1]/img/@src').extract()[0]
                hapiImg = "https://happyhotel.jp" + imgxpath
                item["J_img_url"] = hapiImg
            # ホテル説明
            if len(response.xpath('//*[@id="imgCanvasChanger"]/div[1]/img/@src').extract()) == 0:
                item["K_discribe"] =response.xpath('//*[@id="outline"]/div/p').xpath('string()').get()
            else:
                item["K_discribe"] = response.xpath('//*[@id="outline"]/div[2]/p[2]').xpath('string()').get()
            # 住所
            if len(response.xpath('//*[@id="imgCanvasChanger"]/div[1]/img/@src').extract()) == 0:
                item["C_address"] = response.xpath('//*[@id="outline"]/div/dl/dd[1]').xpath('string()').get()
            else:
                item["C_address"] = response.xpath('//*[@id="outline"]/div[2]/dl/dd[1]').xpath('string()').get()
            # 電話番号
            if len(response.xpath('//*[@id="imgCanvasChanger"]/div[1]/img/@src').extract()) == 0:
                item["D_tel"] = response.xpath('//*[@id="outline"]/div/dl/dd[2]').xpath('string()').get()
            else:
                item["D_tel"] = response.xpath('//*[@id="outline"]/div[2]/dl/dd[2]').xpath('string()').get()
            # マップコード
            if len(response.xpath('//*[@id="imgCanvasChanger"]/div[1]/img/@src').extract()) == 0:
                item["V_map_code"] = response.xpath('//*[@id="outline"]/div/dl/dd[3]').xpath('string()').get().replace('マップコードとは','').replace("\t","").replace('\r',"")
            else:
                item["V_map_code"] = response.xpath('//*[@id="outline"]/div[2]/dl/dd[3]').xpath('string()').get().replace('マップコードとは','')

            # ###################
            # table infomation #
            #####################

            tabelTag = response.css('.tabBody > table')

            # 料金
            payment_setting_list =""
            td_hotel_group_con =""
            td_other_service_con = ""
            td_room_service_con =""
            td_offial_site_con = ""
            room_num_con =""
            park_con =""
            constract_con =""
            access_con =""
            td_facility_con =""
            td_member_service_con =""
            td_payment_con =""
            td_outside_con =""
            td_how_many_con =""
            td_reservation =""
            td_hotel_group_con =""


            for tr in response.css('tr'):
                # td一個分のデータ
                content = tr.xpath('string()')[0].get().replace("\t","").replace('\r',"")

                # print("＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝")
                # ルーム数
                if tr.xpath('string()').re(r'ルーム数'):
                    room_num_con = content.replace('ルーム数',"").replace("\n","")

                # 駐車場
                if tr.xpath('string()').re(r'駐車場'):
                    park_con = content.replace('駐車場',"").replace("\n","")

                # 建物形式
                if tr.xpath('string()').re(r'建物形式'):
                    constract_con = content.replace('建物形式',"").replace("\n","")


                # アクセス
                if tr.xpath('string()').re(r'アクセス'):
                    access_con = content.replace('アクセス',"").replace("\n","")

                # 設備
                if tr.xpath('string()').re(r'設備'):
                    td_facility_con = content.replace('設備',"").replace("\n","")

                # メンバー特典
                if tr.xpath('string()').re(r'メンバー特典'):
                    td_member_service_con = content.replace('メンバー特典',"").replace("\n","")


                # ルームサービス
                if tr.xpath('string()').re(r'ルームサービス'):
                    td_room_service_con = content.replace('ルームサービス',"").replace("\n","")

                # その他サービス
                if tr.xpath('string()').re(r'その他サービス'):
                    td_other_service_con = content.replace('その他サービス',"").replace("\n","")

                # 支払い/クレジットカード
                if tr.xpath('string()').re(r'支払い/クレジットカード'):
                    td_payment_con = content.replace('支払い/クレジットカード',"").replace("\n","")

                # 外出
                if tr.xpath('string()').re(r'外出'):
                    td_outside_con = content.replace('外出',"").replace("\n","")

                # 利用人数
                if tr.xpath('string()').re(r'利用人数'):
                    td_how_many_con = content.replace('利用人数',"").replace("\n","")

                # 予約
                if tr.xpath('string()').re(r'予約'):
                    td_reservation = content.replace('予約',"").replace("\n","")

                # オフィシャルサイト
                if tr.xpath('string()').re(r'オフィシャルサイト'):
                    # td_offial_site_con = content.replace('オフィシャルサイト',"").replace("\n","")
                    td_offial_site_con = tr.css("td").xpath('string()').get().strip()

                # # Twitter
                # if tr.xpath('string()').re(r'Twitter'):
                #     td_twitter_con =tr.css('a::attr(href)').extract()
                #     # td_twitter_con = content.replace('Twitter',"").replace("\n","")

                # ホテルグループ
                if tr.xpath('string()').re(r'ホテルグループ'):
                    td_hotel_group_con = content.replace('ホテルグループ',"").replace("\n","")

                # 料金システム
                if tr.css('.strong').get(default='') != '':
                    price_title = tr.xpath('string()').re(r'\t\S*\r')
                    # print(price_title)
                    if len(price_title) != 0:
                        payment_setting_list +=  "<h4>" + price_title[0].replace("\t","").replace('\r',"") + "</h4>"
                        price_info = tr.xpath('string()').re(r'\t\S*\r')[1:]
                        p = "".join(price_info)
                        payment_setting_list += p.replace('\t','').replace('\r','')


            item["I_td_room_num"] = room_num_con
            item["M_td_park"] = park_con
            item["N_td_construct"] = constract_con
            item["L_td_access"] = access_con
            item["O_td_facility"] = td_facility_con
            item["R_td_member_service"] = td_member_service_con
            item["S_td_room_service"] = td_room_service_con
            item["T_td_other_service"] = td_other_service_con
            item["W_td_payment"] = td_payment_con
            item["U_td_outside"] = td_outside_con
            item["Q_td_how_many"] = td_how_many_con
            item["X_td_reservation"] = td_reservation
            item["E_td_offcial_site"] = td_offial_site_con
            # item["td_twitter"] = td_twitter_con
            item["P_td_hotel_group"] = td_hotel_group_con
            item["Y_td_payment_setting"] = payment_setting_list
            yield item
        except:
            logging.error(traceback.format_exc())
            raise

    def parse_no_hotel(self,response):
        pass

