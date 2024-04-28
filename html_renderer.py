
import sys
# from bonds.re_manager import ReManager
from noocube.re_manager import ReManager
from noocube.re_constants import *
# sys.path.append('/home/ak/projects/2_Proj_TLH_Center/project_tlh') # Прописываем path в системную переменную Python, что бы можно было запускать функции из данного модуля напрямую


# from noocube.search_tlh_manager import SearchTLHManager
from noocube.text_formater import TextFormater
import noocube.funcs_general as FG

from noocube.files_manager import FilesManager


class HTMLRenderer ():

    """Форматирует простой текст в зависимости от разных форматов текста, техгических знаков и мемов в
    HTML - код с определенными заданынми стилями
    formatStyle - задаваемые стили в зависимости от того формата, который подразумевается под текстовым файлом. например, TLH-формат.
    Но могут быть и какие-то другие форматы для стилизации в дркгих проектах
    """


    def __init__(self, inpText, formatStyle = ''):

        self.htmlText = HTMLRenderer.convert_TLHblock_to_HTMLblock(inpText)


    @staticmethod
    def convert_TLHblock_to_HTMLblock(TLHTxt):
        """
        TextFormaterTLH
        Конвертируем текстовый инф.блок TLH из файла в формат HTML (информационную его часть)
        Category: TLH методы
        """
        txtFormatter = TextFormater()


        txtLines = txtFormatter.get_str_lines_of_text(TLHTxt)
        htmlText = ''
        # Цикл по строкам текста. Каждая строка подвергается анализу по нескольким поисковым ворматным фильтрам и, если находится формат, который включает наложение стилей, 
        # то проводится реконструкция строки в зависимсоти от заданного формата и стилей
        for line in txtLines:


            line = line.replace('\n', '<br>')
            line = line.replace('\t', '&emsp;')

            # Накладываем TLH-стиль для ссылки.
            line = HTMLRenderer.replace_href_by_html_link(line) 

            htmlText += line 

        htmlText = '<br>' + htmlText # перевод строки для разделения от заголовка

        # print (htmlText)

        return htmlText




    @staticmethod
    def replace_href_by_html_link(txtLine):
        """
        Заменить фрагмент текста с href-текстом на html-ссылку
        Category: HTML код мейкеры
        """

        if 'https://' in txtLine or 'http://' in txtLine:
            
            hrefLine = txtLine
            clearHrefLine = hrefLine.replace('\n', '')  # .replace('\t', '') # очищаем ссылку от всех ненужных символов
            clearHrefLine = hrefLine

            href = ReManager.find_url_in_string(clearHrefLine)


            brSimbQn = FG.count_str_in_word(hrefLine, '\n')
            brHTMLStr = FG.compose_str_with_repeated_simbol('<br>', brSimbQn) # строка из n <br> для вставки разрывов в HTML


            hrefLine = hrefLine.replace("*","") # Удаляем звездочку
            # brHTMLStr = brHTMLStr.replace("*","") # Удаляем звездочку

            

            htmlLine = f"<a href = '{href}' target = '_balnk'>{hrefLine}</a>{brHTMLStr}"

            
            # hrefLine = hrefLine.replace('\t', '&emsp;')
            hrefLine = hrefLine.replace(href, htmlLine)

            hrefHTMLLine = hrefLine

            return hrefHTMLLine

        else:
            return txtLine




    @staticmethod
    def render_comp_analisys_tlh_data_in_comp_analisys_temlate1_html(TLHTxt, temlateFile):
        """
        TextFormaterTLH
        Конвертировать текстовый tlh-блок  с анализом компании-эмитента в формат HTML на основе шаблона в файле
        temlateFile - абсолютный путь к шаблону для данного метода для рендеринга
        '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/templates/html_formats/bond_inf_temlate1.html'
        Category: TLH методы
        """
        
        # Инициализация
        txtFormatter = TextFormater()
        fm = FilesManager(temlateFile)

        # txtLines = txtFormatter.get_str_lines_of_text(TLHTxt)
        # # print(f"PR_952 --> txtLines = {txtLines}")  
        
        # A. Парсим TLHTxt текст и получаем нужные данные
        
        # B. Название компании
        startMark = 'НАЗВАНИЕ КОМПАНИИ'
        endMark = '--'
        compName, startIdx, endIdx = txtFormatter.find_in_text_fragment_by_start_end_marks (TLHTxt, startMark, endMark)
        compName = compName.replace(startMark,'').replace('--','').replace('- ','')
        
        # C. ИНН компании
        startMark = 'ИНН'
        endMark = '--'
        compInn, startIdx, endIdx = txtFormatter.find_in_text_fragment_by_start_end_marks (TLHTxt, startMark, endMark)
        compInn = compInn.replace(startMark,'').replace('--','').replace('- ','')
        
        # D. ОКПО компании
        startMark = 'ОКПО'
        endMark = '--'
        compOkpo, startIdx, endIdx = txtFormatter.find_in_text_fragment_by_start_end_marks (TLHTxt, startMark, endMark)
        compOkpo = compOkpo.replace(startMark,'').replace('--','').replace('- ','')
        
        # E. КЛЮЧЕВЫЕ ХАРАКТЕРИСТИКИ компании
        startMark = 'КЛЮЧЕВЫЕ ХАРАКТЕРИСТИКИ'
        endMark = '--'
        compCharacteristics, startIdx, endIdx = txtFormatter.find_in_text_fragment_by_start_end_marks (TLHTxt, startMark, endMark)
        compCharacteristics = compCharacteristics.replace(startMark,'').replace('--','').replace('- ','')
        
        # F. КАТЕГОРИЯ компании
        startMark = 'КАТЕГОРИЯ'
        endMark = '--'
        compCategory, startIdx, endIdx = txtFormatter.find_in_text_fragment_by_start_end_marks (TLHTxt, startMark, endMark)
        compCategory = compCategory.replace(startMark,'').replace('--','').replace('- ','')
        
        
        # G. Плюсы компании
        startMark = 'Плюсы:'
        endMark = '....'
        compPluses, startIdx, endIdx = txtFormatter.find_in_text_fragment_by_start_end_marks (TLHTxt, startMark, endMark)
        compPluses = compPluses.replace(startMark,'')
        parts = compPluses.split('- ')
        cPluses = '<br>'.join(parts).replace('<br>', '', 1)
        
        
        # G. Минусы компании
        startMark = 'Минусы:'
        endMark = '....'
        compMinuses, startIdx, endIdx = txtFormatter.find_in_text_fragment_by_start_end_marks (TLHTxt, startMark, endMark)
        compMinuses = compMinuses.replace(startMark,'')
        parts = compMinuses.split('- ')
        cMinuses = '<br>'.join(parts).replace('<br>', '', 1)
        
        
        # H. Уставной капитал компании
        startMark = 'Уставный капитал:'
        endMark = '-'
        compAuthCapital, startIdx, endIdx = txtFormatter.find_in_text_fragment_by_start_end_marks (TLHTxt, startMark, endMark)
        compAuthCapital = compAuthCapital.replace(startMark,'')
        
        
        # I. Дата регистрации компании
        startMark = 'Дата регистрации:'
        endMark = '-'
        compRegistrDate, startIdx, endIdx = txtFormatter.find_in_text_fragment_by_start_end_marks (TLHTxt, startMark, endMark)
        compRegistrDate = compRegistrDate.replace(startMark,'')
        
        
        # J. сайт компании
        startMark = 'Сайт:'
        endMark = '....'
        compSite, startIdx, endIdx = txtFormatter.find_in_text_fragment_by_start_end_marks (TLHTxt, startMark, endMark)
        compSite = compSite.replace(startMark,'')
        if 'https' in compSite or 'http' in compSite:
            compSite = f"<a href='{compSite}' target='_blank'>{compSite}</a>"
        
        
        # K. Кол-во выпусков облигаций компании
        startMark = 'Выпуски облигаций на рынке:'
        endMark = '-'
        compBondsIssues, startIdx, endIdx = txtFormatter.find_in_text_fragment_by_start_end_marks (TLHTxt, startMark, endMark)
        compBondsIssues = compBondsIssues.replace(startMark,'')
        
        
        # L.Численность работников компании
        startMark = 'Численность работников:'
        endMark = '-'
        compWorkers, startIdx, endIdx = txtFormatter.find_in_text_fragment_by_start_end_marks (TLHTxt, startMark, endMark)
        compWorkers = compWorkers.replace(startMark,'')
        
        
        
        # M.Финансы компании
        startMark = 'Финансы:'
        endMark = '....'
        cFinance, startIdx, endIdx = txtFormatter.find_in_text_fragment_by_start_end_marks (TLHTxt, startMark, endMark)
        # compFinance = compFinance.replace(startMark,'')
        # parts = compFinance.split('-')
        cFinance = '<br>'.join(parts).replace('<br>', '', 1)
        
        
        
        # N.Товарные знаки компании
        startMark = 'Товарные знаки:'
        endMark = '-'
        compTradeMarks, startIdx, endIdx = txtFormatter.find_in_text_fragment_by_start_end_marks (TLHTxt, startMark, endMark)
        compTradeMarks = compTradeMarks.replace(startMark,'')
        
        
        
        
        # O.Участник системы госзакупок
        startMark = 'Участник системы госзакупок:'
        endMark = '-'
        compGosZakup, startIdx, endIdx = txtFormatter.find_in_text_fragment_by_start_end_marks (TLHTxt, startMark, endMark)
        compGosZakup = compGosZakup.replace(startMark,'')
        
        
        # P.Рэнкинг компании
        startMark = 'Рэнкинг:'
        endMark = '....'
        cRanking, startIdx, endIdx = txtFormatter.find_in_text_fragment_by_start_end_marks (TLHTxt, startMark, endMark)
        # compRanking = compRanking.replace(startMark,'')
        # parts = compRanking.split('-')
        cRanking = cRanking.replace(startMark,'')
        
        
        # R.Новости и информация
        startMark = 'Новости и информация:'
        endMark = '....'
        cNews, startIdx, endIdx = txtFormatter.find_in_text_fragment_by_start_end_marks (TLHTxt, startMark, endMark)
        cNews = cNews.replace(startMark,'')
        parts = cNews.split('-')
        cNews = '<br>'.join(parts).replace('<br>', '', 1)
        
        
        
        # S.Участник системы госзакупок
        startMark = 'Акции:'
        endMark = '-'
        compStocks, startIdx, endIdx = txtFormatter.find_in_text_fragment_by_start_end_marks (TLHTxt, startMark, endMark)
        compStocks = compStocks.replace(startMark,'')
        
        
        
        
        # T.Ссылки по компании
        startMark = 'Ссылки:'
        endMark = '...'
        compLinks, startIdx, endIdx = txtFormatter.find_in_text_fragment_by_start_end_marks (TLHTxt, startMark, endMark)
        compLinks = compLinks.replace(startMark,'')
        parts = compLinks.split('~')
        cLinks = '<br>'.join(parts).replace('<br>', '', 1)
        
        
        
        # U. РЕЙТИНГИ компании
        startMark = 'РЕЙТИНГИ:'
        endMark = '....'
        cRatings, startIdx, endIdx = txtFormatter.find_in_text_fragment_by_start_end_marks (TLHTxt, startMark, endMark)
        cRatings = cRatings.replace(startMark,'')
        parts = cRatings.split('- ')
        cRatings = '<br>'.join(parts).replace('<br>', '', 1)
        
        
        # W. Собственный коэфф компании
        startMark = 'Self koeff:'
        endMark = '-'
        compSelfCoeff, startIdx, endIdx = txtFormatter.find_in_text_fragment_by_start_end_marks (TLHTxt, startMark, endMark)
        compSelfCoeff = compSelfCoeff.replace(startMark,'')
        
        
        
        # X. Коэфф Fapvdo компании
        startMark = 'FapVdo koeff:'
        endMark = '....'
        compFapvdoCoeff, startIdx, endIdx = txtFormatter.find_in_text_fragment_by_start_end_marks (TLHTxt, startMark, endMark)
        compFapvdoCoeff = compFapvdoCoeff.replace(startMark,'')
        
        
        # print(f"PR_953 --> compName = {compName}")  
        
        # Y. Замещение в шаблоне htmlText маркеров данных компании, полученными  из парсинга TLH-текста с анализом компании
        
        # Изначальный html-код шаблона для аналитических данных по компании
        htmlText = fm.read_file_data_txt()
        
        htmlText = htmlText.replace('%%COMP_NAME%%', compName)
        htmlText = htmlText.replace('%%COMP_INN%%', compInn)
        htmlText = htmlText.replace('%%COMP_OKPO%%', compOkpo)
        htmlText = htmlText.replace('%%COMP_CHARACTERISTICS%%', compCharacteristics)
        htmlText = htmlText.replace('%%COMP_CATEGORY%%', compCategory)
        htmlText = htmlText.replace('%%COMP_PLUSES%%', cPluses)
        htmlText = htmlText.replace('%%COMP_MINUSES%%', cMinuses)
        htmlText = htmlText.replace('%%COMP_AUTH_CAPITAL%%', compAuthCapital)
        htmlText = htmlText.replace('%%COMP_REGISTR_DATE%%', compRegistrDate)
        htmlText = htmlText.replace('%%COMP_SITE%%', compSite)
        htmlText = htmlText.replace('%%COMP_BONDS_ISSUES%%', compBondsIssues)
        htmlText = htmlText.replace('%%COMP_WORKERS%%', compWorkers)
        htmlText = htmlText.replace('%%COMP_FINANCE%%', cFinance)
        htmlText = htmlText.replace('%%COMP_TRADE_MARKS%%', compTradeMarks)
        htmlText = htmlText.replace('%%COMP_GOS_ZAKUP%%', compGosZakup)
        htmlText = htmlText.replace('%%COMP_RANKING%%', cRanking)
        htmlText = htmlText.replace('%%COMP_NEWS%%', cNews)
        htmlText = htmlText.replace('%%COMP_STOCKS%%', compStocks)
        htmlText = htmlText.replace('%%COMP_LINKS%%', cLinks)
        htmlText = htmlText.replace('%%COMP_RATINGS%%', cRatings)
        htmlText = htmlText.replace('%%COMP_SELF_COEFF%%', compSelfCoeff)
        htmlText = htmlText.replace('%%COMP_FAPVDO_COEFF%%', compFapvdoCoeff)

        return htmlText








    @staticmethod
    def render_bond_analisys_tlh_data_in_bond_analisys_temlate1_html(TLHTxt, temlateFile):
        """
        TextFormaterTLH
        Конвертировать текстовый tlh-блок  с анализом  заданной облигации в формат HTML на основе шаблона в файле
        temlateFile - абсолютный путь к шаблону для данного метода для рендеринга
        '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/templates/html_formats/bond_analisys_temlate1.html'
        Category: TLH методы
        """
        
        # Инициализация
        txtFormatter = TextFormater()
        fm = FilesManager(temlateFile)

        # txtLines = txtFormatter.get_str_lines_of_text(TLHTxt)
        # # print(f"PR_952 --> txtLines = {txtLines}")  
        
        # A. Парсим TLHTxt текст и получаем нужные данные
        
        
        # T. Дата на которую считана облигация из Инета
        startMark = '--> ОБЛИГАЦИЯ'
        endMark = ')'
        bondAnalisysDate, startIdx, endIdx = txtFormatter.find_in_text_fragment_by_start_end_marks (TLHTxt, startMark, endMark)
        bondAnalisysDate = bondAnalisysDate.replace(startMark,'').replace('(на ', '').replace(')', '')
        
        
        # B. ИСИН облигации
        startMark = 'ИСИН:'
        endMark = '-'
        bondIsin, startIdx, endIdx = txtFormatter.find_in_text_fragment_by_start_end_marks (TLHTxt, startMark, endMark)
        bondIsin = bondIsin.replace(startMark,'')
        
        
        # C. Ник облигации
        startMark = 'Ник облигации:'
        endMark = '-'
        bondNickName, startIdx, endIdx = txtFormatter.find_in_text_fragment_by_start_end_marks (TLHTxt, startMark, endMark)
        bondNickName = bondNickName.replace(startMark,'')
        
        
        # D. Квалификация по облигации
        startMark = 'Квалификация:'
        endMark = '-'
        bondCualification, startIdx, endIdx = txtFormatter.find_in_text_fragment_by_start_end_marks (TLHTxt, startMark, endMark)
        bondCualification = bondCualification.replace(startMark,'')
        
        
        
        # E. Текущая цена облигации
        startMark = 'Текущая цена:'
        endMark = '-'
        bondCurrPrice, startIdx, endIdx = txtFormatter.find_in_text_fragment_by_start_end_marks (TLHTxt, startMark, endMark)
        bondCurrPrice = bondCurrPrice.replace(startMark,'')
        
        
        
        # F. Текущая цена облигации
        startMark = 'ГКД:'
        endMark = '-'
        bondGKD, startIdx, endIdx = txtFormatter.find_in_text_fragment_by_start_end_marks (TLHTxt, startMark, endMark)
        bondGKD = bondGKD.replace(startMark,'')
        
        
        # G. Купон облигации
        startMark = 'Купон:'
        endMark = '-'
        bondCoupon, startIdx, endIdx = txtFormatter.find_in_text_fragment_by_start_end_marks (TLHTxt, startMark, endMark)
        bondCoupon = bondCoupon.replace(startMark,'')
        
        
        
        # H. Номинал облигации
        startMark = 'Номинал:'
        endMark = '-'
        bondNominal, startIdx, endIdx = txtFormatter.find_in_text_fragment_by_start_end_marks (TLHTxt, startMark, endMark)
        bondNominal = bondNominal.replace(startMark,'')
        
        
        
        # I. Окупаемость облигации
        startMark = 'Окупаемость:'
        endMark = '-'
        bondPaybackPeriod, startIdx, endIdx = txtFormatter.find_in_text_fragment_by_start_end_marks (TLHTxt, startMark, endMark)
        bondPaybackPeriod = bondPaybackPeriod.replace(startMark,'')
        
        
        # J. Частота облигации
        startMark = 'Частота:'
        endMark = '-'
        bondFrequency, startIdx, endIdx = txtFormatter.find_in_text_fragment_by_start_end_marks (TLHTxt, startMark, endMark)
        bondFrequency = bondFrequency.replace(startMark,'')
        
        
        # K. Срок погашения облигации
        startMark = 'Срок погашения:'
        endMark = '-'
        bondExpiration, startIdx, endIdx = txtFormatter.find_in_text_fragment_by_start_end_marks (TLHTxt, startMark, endMark)
        bondExpiration = bondExpiration.replace(startMark,'')
        
        
        
        # L. Доходность к погашению облигации
        startMark = 'Доходность к погашению:'
        endMark = '-'
        bondExpirationYield, startIdx, endIdx = txtFormatter.find_in_text_fragment_by_start_end_marks (TLHTxt, startMark, endMark)
        bondExpirationYield = bondExpirationYield.replace(startMark,'')
        
        
        # M. Дата размещения облигации
        startMark = 'Доходность к погашению:'
        endMark = '-'
        bondStartDate, startIdx, endIdx = txtFormatter.find_in_text_fragment_by_start_end_marks (TLHTxt, startMark, endMark)
        bondStartDate = bondStartDate.replace(startMark,'')
        
        
        # N. Дата выплаты ближайшего купона облигации
        startMark = 'Дата выплаты ближайшего купона:'
        endMark = '-'
        bondNextCouponDate, startIdx, endIdx = txtFormatter.find_in_text_fragment_by_start_end_marks (TLHTxt, startMark, endMark)
        bondNextCouponDate = bondNextCouponDate.replace(startMark,'')
        
        
        # O. Дней до выплаты следующего купона облигации
        startMark = 'Дней до выплаты следующего купона:'
        endMark = '-'
        bondNextCouponDays, startIdx, endIdx = txtFormatter.find_in_text_fragment_by_start_end_marks (TLHTxt, startMark, endMark)
        bondNextCouponDays = bondNextCouponDays.replace(startMark,'')
        
        
        
        # P. Оферта по облигации
        startMark = 'Оферта:'
        endMark = '....'
        bondOferta, startIdx, endIdx = txtFormatter.find_in_text_fragment_by_start_end_marks (TLHTxt, startMark, endMark)
        bondOferta = bondOferta.replace(startMark,'')
        
        
        
        # Q. Амортизация по облигации
        startMark = 'Амортизация:'
        endMark = '....'
        bondAmortization, startIdx, endIdx = txtFormatter.find_in_text_fragment_by_start_end_marks (TLHTxt, startMark, endMark)
        bondAmortization = bondAmortization.replace(startMark,'')
        
        
        
        # R. Амортизация по облигации
        startMark = 'Переменный купон:'
        endMark = '....'
        bondChangableCoupon, startIdx, endIdx = txtFormatter.find_in_text_fragment_by_start_end_marks (TLHTxt, startMark, endMark)
        bondChangableCoupon = bondChangableCoupon.replace(startMark,'')
        
        
        # S. Форумы по облигации
        startMark = 'Форумы:'
        endMark = '....'
        bondForums, startIdx, endIdx = txtFormatter.find_in_text_fragment_by_start_end_marks (TLHTxt, startMark, endMark)
        bondForums = bondForums.replace(startMark,'')
        
        
        # S. РЕШЕНИЕ О ВНЕСЕНИИ В ПАКЕТ по облигации
        startMark = 'РЕШЕНИЕ О ВНЕСЕНИИ В ПАКЕТ:'
        endMark = '....'
        bondDesision, startIdx, endIdx = txtFormatter.find_in_text_fragment_by_start_end_marks (TLHTxt, startMark, endMark)
        bondDesision = bondDesision.replace(startMark,'')
        
        
        
        # print(f"PR_953 --> compName = {compName}")  
        
        # Y. Замещение в шаблоне htmlText маркеров данных компании, полученными  из парсинга TLH-текста с анализом компании
        
        # Изначальный html-код шаблона для аналитических данных по компании
        htmlText = fm.read_file_data_txt()
        
        # htmlText = htmlText.replace('%%COMP_NAME%%', compName)
        # htmlText = htmlText.replace('%%COMP_INN%%', compInn)
        # htmlText = htmlText.replace('%%COMP_OKPO%%', compOkpo)
        
        htmlText = htmlText.replace('%%DATE%%', bondAnalisysDate)
        htmlText = htmlText.replace('%%ISIN%%', bondIsin)
        htmlText = htmlText.replace('%%BOND_NICK%%', bondNickName)
        htmlText = htmlText.replace('%%QUALIFICATION%%', bondCualification)
        htmlText = htmlText.replace('%%CURR_PRICE%%', bondCurrPrice)
        htmlText = htmlText.replace('%%BOND_GKD%%', bondGKD)
        htmlText = htmlText.replace('%%COUPON%%', bondCoupon)
        htmlText = htmlText.replace('%%NOMINAL%%', bondNominal)
        htmlText = htmlText.replace('%%PAYBACK_COUPON_PERIOD%%', bondPaybackPeriod)
        htmlText = htmlText.replace('%%BOND_FREQUENCY%%', bondFrequency)
        htmlText = htmlText.replace('%%SROK%%', bondExpiration)
        htmlText = htmlText.replace('%%EXPIRATION_YIELD%%', bondExpirationYield)
        htmlText = htmlText.replace('%%START_DATE%%', bondStartDate)
        htmlText = htmlText.replace('%%NEXT_PAY%%', bondNextCouponDate)
        htmlText = htmlText.replace('%%DAYS_TO_NEXT_PAY%%', bondNextCouponDays)
        htmlText = htmlText.replace('%%OFERTA%%', bondOferta)
        htmlText = htmlText.replace('%%AMORTIZATION%%', bondAmortization)
        htmlText = htmlText.replace('%%CHANGABLE_COUPON%%', bondChangableCoupon)
        htmlText = htmlText.replace('%%FORUMS%%', bondForums)
        htmlText = htmlText.replace('%%DESICION%%', bondDesision)
        
        
        
        

        # htmlText = f""" 
        #     <p><strong>ОБЛИГАЦИЯ</strong> (на {bondAnalisysDate})</p>
        #     <p><strong>ИСИН</strong>: {bondIsin}<br/>
        #     <strong>Ник облигации:</strong> {bondNickName}<br/>
        #     <strong>Квалификация</strong>: {bondCualification}<br/>
        #     <strong>Текущая цена</strong>: {bondCurrPrice}<br/>
        #     <strong>ГКД</strong>: {bondGKD}<br/>
        #     <strong>Купон</strong>: {bondCoupon}<br/>
        #     <strong>Номинал</strong>: {bondNominal}<br/>
        #     <strong>Окупаемость</strong>: = {bondPaybackPeriod} купонного периода <br/>
        #     <strong>Частота</strong>: {bondFrequency}<br/>
        #     <strong>Срок погашения</strong>: {bondExpiration}<br/>
        #     <strong>Доходность к погашению</strong>: {bondExpirationYield}<br/>
        #     <strong>Дата размещения</strong>: {bondStartDate}<br/>
        #     <strong>Дата выплаты ближайшего купона</strong>: {bondNextCouponDate}<br/>
        #     <strong>Дней до выплаты следующего купона</strong>: {bondNextCouponDays}</p>
        #     <p><strong>Оферта:</strong> {bondOferta}</p>
        #     <p></p>
        #     <p><strong>Амортизация:</strong> {bondAmortization}</p>
        #     <p></p>
        #     <p><strong>Переменный купон:</strong> {bondChangableCoupon}</p>
        #     <p>-</p>
        #     <p><strong>Форумы</strong>:</p>
        #     <p>{bondForums}</p>
        #     <p><br /><strong>РЕШЕНИЕ О ВНЕСЕНИИ В ПАКЕТ:</strong></p>
        #     <p>{bondDesision}</p>
        # """
        

        return htmlText
















