import pandas as pd
from flask import Blueprint, render_template, jsonify, request
from snownlp import SnowNLP

from dao import articleDao, commentDao
from util import wordcloudUtil, mapUtil

pb = Blueprint('page', __name__, url_prefix='/page', template_folder='templates')


@pb.route('/home')
def home():
    """
    进入主页面，获取相应的数据，带到页面去
    :return:
    """
    articleData = articleDao.get7DayArticle()
    xAxis7ArticleData = []
    yAxis7ArticleData = []
    for article in articleData:
        xAxis7ArticleData.append(article[0])
        yAxis7ArticleData.append(article[1])

    # 获取帖子类别数量
    arcTypeData = []
    articleTypeAmountList = articleDao.getArticleTypeAmount()
    for arcType in articleTypeAmountList:
        arcTypeData.append({'value': arcType[1], 'name': arcType[0]})

    # 获取top50评论用户名
    top50CommentUserList = commentDao.getTopCommentUser()
    top50CommentUserNameList = [cu[0] for cu in top50CommentUserList]
    str = ' '.join(top50CommentUserNameList)
    wordcloudUtil.genWordCloudPic(str, 'comment_mask.jpg', 'comment_user_cloud.jpg')

    # 获取7天评论数量
    commentData = []
    commentAmountList = commentDao.getCommentAmount()
    for comment in commentAmountList:
        commentData.append({'value': comment[1], 'name': comment[0]})
    return render_template('index.html',
                           xAxis7ArticleData=xAxis7ArticleData,
                           yAxis7ArticleData=yAxis7ArticleData,
                           arcTypeData=arcTypeData,
                           commentData=commentData)


@pb.route('homePageData')
def getHomePageData():
    """
    获取主页数据 ajax异步交互 前端每隔5分钟请求一次 实时数据
    :return:
    """
    totalArticle = articleDao.getTotalArticle()
    topAuthor = articleDao.getTopAuthor()
    topRegion = articleDao.getTopRegion()
    topArticles = articleDao.getArticleTopZan()
    return jsonify(totalArticle=totalArticle, topAuthor=topAuthor, topRegion=topRegion, topArticles=topArticles)


@pb.route('hotWord')
def hotWord():
    """
    热词分析统计
    :return:
    """
    hotwordList = []
    # 只读取前100条
    df = pd.read_csv('./fenci/comment_fre.csv', nrows=100)
    for value in df.values:
        hotwordList.append(value[0])
    # 获取请求参数，如果没有获取到，给个默认值 第一个列表数据
    defaultHotWord = request.args.get('word', default=hotwordList[0])
    hotwordNum = 0  # 出现次数
    for value in df.values:
        if defaultHotWord == value[0]:
            hotwordNum = value[1]

    # 情感分析
    sentiments = ''
    stc = SnowNLP(defaultHotWord).sentiments
    if stc > 0.6:
        sentiments = '正面'
    elif stc < 0.2:
        sentiments = '负面'
    else:
        sentiments = '中性'

    commentHotWordData = commentDao.getCommentHotWordAmount(defaultHotWord)
    xAxisHotWordData = []
    yAxisHotWordData = []
    for comment in commentHotWordData:
        xAxisHotWordData.append(comment[0])
        yAxisHotWordData.append(comment[1])

    commentList = commentDao.getCommentByHotWord(defaultHotWord)
    return render_template('hotWord.html',
                           hotwordList=hotwordList,
                           defaultHotWord=defaultHotWord,
                           hotwordNum=hotwordNum,
                           sentiments=sentiments,
                           xAxisHotWordData=xAxisHotWordData,
                           yAxisHotWordData=yAxisHotWordData,
                           commentList=commentList)


@pb.route('articleData')
def articleData():
    """
    微博舆情分析
    :return:
    """
    articleOldList = articleDao.getAllArticle()
    articleNewList = []
    for article in articleOldList:
        article = list(article)
        # 情感分析
        sentiments = ''
        stc = SnowNLP(article[1]).sentiments
        if stc > 0.6:
            sentiments = '正面'
        elif stc < 0.2:
            sentiments = '负面'
        else:
            sentiments = '中性'
        article.append(sentiments)
        articleNewList.append(article)
    return render_template('articleData.html', articleList=articleNewList)


@pb.route('articleDataAnalysis')
def articleDataAnalysis():
    """
    微博数据分析
    :return:
    """
    arcTypeList = []
    df = pd.read_csv('./spider/arcType_data.csv')
    for value in df.values:
        arcTypeList.append(value[0])
    # 获取请求参数，如果没有获取到，给个默认值 第一个列表数据
    defaultArcType = request.args.get('arcType', default=arcTypeList[0])
    articleList = articleDao.getArticleByArcType(defaultArcType)
    xDzData = []  # 点赞x轴数据
    xPlData = []  # 评论x轴数据
    xZfData = []  # 转发x轴数据
    rangeNum = 1000
    rangeNum2 = 100
    for item in range(0, 10):
        xDzData.append(str(rangeNum * item) + '-' + str(rangeNum * (item + 1)))
        xPlData.append(str(rangeNum * item) + '-' + str(rangeNum * (item + 1)))
    for item in range(0, 20):
        xZfData.append(str(rangeNum2 * item) + '-' + str(rangeNum2 * (item + 1)))
    xDzData.append('1万+')
    xPlData.append('1万+')
    xZfData.append('2千+')
    yDzData = [0 for x in range(len(xDzData))]  # 点赞y轴数据
    yPlData = [0 for x in range(len(xPlData))]  # 评论y轴数据
    yZfData = [0 for x in range(len(xZfData))]  # 转发y轴数据
    for article in articleList:
        for item in range(len(xDzData)):
            if int(article[4]) < rangeNum * (item + 1):
                yDzData[item] += 1
                break
            elif int(article[4]) > 10000:
                yDzData[len(xDzData) - 1] += 1
                break
            if int(article[3]) < rangeNum * (item + 1):
                yPlData[item] += 1
                break
            elif int(article[3]) > 10000:
                yPlData[len(xDzData) - 1] += 1
                break

    for article in articleList:
        for item in range(len(xZfData)):
            if int(article[2]) < rangeNum2 * (item + 1):
                yZfData[item] += 1
                break
            elif int(article[2]) > 2000:
                yZfData[len(xZfData) - 1] += 1
                break
    return render_template('articleDataAnalysis.html',
                           arcTypeList=arcTypeList,
                           defaultArcType=defaultArcType,
                           xDzData=xDzData,
                           yDzData=yDzData,
                           xPlData=xPlData,
                           yPlData=yPlData,
                           xZfData=xZfData,
                           yZfData=yZfData)


@pb.route('commentDataAnalysis')
def commentDataAnalysis():
    """
    微博评论数据分析
    :return:
    """
    commentList = commentDao.getAllComment()
    xDzData = []  # 点赞X轴数据
    rangeNum = 5
    for item in range(0, 20):
        xDzData.append(str(rangeNum * item) + '-' + str(rangeNum * (item + 1)))
    xDzData.append('1百+')
    yDzData = [0 for x in range(len(xDzData))]  # 点赞y轴数据
    genderDic = {'男': 0, '女': 0}
    for comment in commentList:
        for item in range(len(xDzData)):
            if int(comment[4]) < rangeNum * (item + 1):
                yDzData[item] += 1
                break
            elif int(comment[4]) > 100:
                yDzData[len(xDzData) - 1] += 1
                break
            if genderDic.get(comment[8], -1) != -1:
                genderDic[comment[8]] += 1
    genderData = [{'name': x[0], 'value': x[1]} for x in genderDic.items()]

    # 只读取前50条数据
    df = pd.read_csv('./fenci/comment_fre.csv', nrows=50)
    hotCommentwordList = [x[0] for x in df.values]
    str2 = ' '.join(hotCommentwordList)
    wordcloudUtil.genWordCloudPic(str2, 'comment_mask.jpg', 'comment_cloud.jpg')
    return render_template('commentDataAnalysis.html',
                           xDzData=xDzData,
                           yDzData=yDzData,
                           genderData=genderData)


@pb.route('articleCloud')
def articleCloud():
    """
    微博内容词云图
    :return:
    """
    # 只读取前50条数据
    df = pd.read_csv('./fenci/article_fre.csv', nrows=50)
    hotArticlewordList = [x[0] for x in df.values]
    str2 = ' '.join(hotArticlewordList)
    wordcloudUtil.genWordCloudPic(str2, 'article_mask.jpg', 'article_cloud.jpg')
    return render_template('articleCloud.html')


@pb.route('commentCloud')
def commentCloud():
    """
    微博评论词云图
    :return:
    """
    # 只读取前50条数据
    df = pd.read_csv('./fenci/comment_fre.csv', nrows=50)
    hotCommentwordList = [x[0] for x in df.values]
    str2 = ' '.join(hotCommentwordList)
    wordcloudUtil.genWordCloudPic(str2, 'comment_mask.jpg', 'comment_cloud.jpg')
    return render_template('commentCloud.html')


@pb.route('commentUserCloud')
def commentUserCloud():
    """
    微博评论用户词云图
    :return:
    """
    # 获取top50评论用户名
    top50CommentUserList = commentDao.getTopCommentUser()
    top50CommentUserNameList = [cu[0] for cu in top50CommentUserList]
    str = ' '.join(top50CommentUserNameList)
    wordcloudUtil.genWordCloudPic(str, 'comment_mask.jpg', 'comment_user_cloud.jpg')
    return render_template('commentUserCloud.html')


@pb.route('ipDataAnalysis')
def ipDataAnalysis():
    """
    IP地址数据分析
    :return:
    """
    cityDic = {}  # 微博文章作者IP
    cityList = mapUtil.cityList
    articleList = articleDao.getAllArticle()
    for article in articleList:
        if article[5]:
            for city in cityList:
                if city['province'].find(article[5]) != -1:
                    if cityDic.get(city['province'], -1) == -1:
                        cityDic[city['province']] = 1
                    else:
                        cityDic[city['province']] += 1
    articleCityDicList = [{'name': x[0], 'value': x[1]} for x in cityDic.items()]

    cityDic2 = {}  # 微博评论作者IP
    commentList = commentDao.getAllComment()
    for comment in commentList:
        if comment[3]:
            for city in cityList:
                if city['province'].find(comment[3]) != -1:
                    if cityDic2.get(city['province'], -1) == -1:
                        cityDic2[city['province']] = 1
                    else:
                        cityDic2[city['province']] += 1
    commentCityDicList = [{'name': x[0], 'value': x[1]} for x in cityDic2.items()]
    return render_template('ipDataAnalysis.html',
                           articleCityDicList=articleCityDicList,
                           commentCityDicList=commentCityDicList)


@pb.route('sentimentAnalysis')
def sentimentAnalysis():
    """
    舆情数据分析
    :return:
    """
    xHotBarData = ['正面', '中性', '负面']
    yHotBarData = [0, 0, 0]
    # 只读取前100条
    df = pd.read_csv('./fenci/comment_fre.csv', nrows=100)
    for value in df.values:
        # 情感分析
        stc = SnowNLP(value[0]).sentiments
        if stc > 0.6:
            yHotBarData[0] += 1
        elif stc < 0.2:
            yHotBarData[2] += 1
        else:
            yHotBarData[1] += 1

    hotTreeMapData = [{
        'name': xHotBarData[0],
        'value': yHotBarData[0]
    }, {
        'name': xHotBarData[1],
        'value': yHotBarData[1]
    }, {
        'name': xHotBarData[2],
        'value': yHotBarData[2]
    }]

    commentPieData = [{
        'name': '正面',
        'value': 0
    }, {
        'name': '中性',
        'value': 0
    }, {
        'name': '负面',
        'value': 0
    }]
    articlePieData = [{
        'name': '正面',
        'value': 0
    }, {
        'name': '中性',
        'value': 0
    }, {
        'name': '负面',
        'value': 0
    }]
    commentList = commentDao.getAllComment()
    for comment in commentList:
        # 情感分析
        stc = SnowNLP(comment[1]).sentiments
        if stc > 0.6:
            commentPieData[0]['value'] += 1
        elif stc < 0.2:
            commentPieData[2]['value'] += 1
        else:
            commentPieData[1]['value'] += 1

    articleList = articleDao.getAllArticle()
    for article in articleList:
        # 情感分析
        stc = SnowNLP(article[1]).sentiments
        if stc > 0.6:
            articlePieData[0]['value'] += 1
        elif stc < 0.2:
            articlePieData[2]['value'] += 1
        else:
            articlePieData[1]['value'] += 1

    df2 = pd.read_csv('./fenci/comment_fre.csv', nrows=15)
    xhotData15 = [x[0] for x in df2.values][::-1]
    yhotData15 = [x[1] for x in df2.values][::-1]
    return render_template('sentimentAnalysis.html',
                           xHotBarData=xHotBarData,
                           yHotBarData=yHotBarData,
                           hotTreeMapData=hotTreeMapData,
                           commentPieData=commentPieData,
                           articlePieData=articlePieData,
                           xhotData15=xhotData15,
                           yhotData15=yhotData15)
