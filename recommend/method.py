# -*- coding: utf-8 -*-
import math
import random
import item_cf
import lfm
import slope_one
import user_cf
import sys
sys.path.append("..")
import data_base


def generate_data_100k_implicit(k):
    """
    :param k: 数据集编号
    """
    global train, test
    train = {}
    test = {}
    for row in open("F:/Machine_learning/Program/system/recommend/ml-100k/u%s.base" % k, "rU"):
        user, item, rating, _ = row.split('\t')
        user, item, rating = int(user), int(item), int(rating)
        train.setdefault(user, {})
        train[user][item] = 1
    for row in open("F:/Machine_learning/Program/system/recommend/ml-100k/u%s.test" % k, "rU"):
        user, item, rating, _ = row.split('\t')
        user, item, rating = int(user), int(item), int(rating)
        test.setdefault(user, {})
        test[user][item] = 1
    global _n, _user_k, _item_k
    _n = 10
    _user_k = 50
    _item_k = 10


def generate_data_100k_explicit(k):
    """
    :param k: 数据集编号
    """
    global train, test
    train = {}
    test = {}
    for row in open("F:/Machine_learning/Program/system/recommend/ml-100k/u%s.base" % k, "rU"):
        user, item, rating, _ = row.split('\t')
        user, item, rating = int(user), int(item), int(rating)
        train.setdefault(user, {})
        train[user][item] = rating
    for row in open("F:/Machine_learning/Program/system/recommend/ml-100k/u%s.test" % k, "rU"):
        user, item, rating, _ = row.split('\t')
        user, item, rating = int(user), int(item), int(rating)
        test.setdefault(user, {})
        test[user][item] = rating
def get_train():
    train = data_base.create_train()
    return train

def generate_matrix(implicit):
    """
    :param implicit: 训练集类型
    """
    #user_cf.user_similarity_cosine(train, iif=False, implicit=implicit)
    # user_cf.user_similarity_cosine(train, iif=True, implicit=implicit)
    # user_cf.user_similarity_jaccard(train, iif=False, implicit=implicit)
    # user_cf.user_similarity_jaccard(train, iif=True, implicit=implicit)
    #user_cf.user_similarity_pearson(train, iif=False, implicit=False)
    # user_cf.user_similarity_pearson(train, iif=True, implicit=False)
    # user_cf.user_similarity_adjusted_cosine(train, iif=False, implicit=False)
    # user_cf.user_similarity_adjusted_cosine(train, iif=True, implicit=False)
    # user_cf.user_similarity_log_likelihood(train, implicit=True)
    # item_cf.item_similarity_cosine(train, norm=False, iuf=False, implicit=implicit)
    # item_cf.item_similarity_cosine(train, norm=True, iuf=False, implicit=implicit)
    # item_cf.item_similarity_cosine(train, norm=False, iuf=True, implicit=implicit)
    # item_cf.item_similarity_jaccard(train, norm=False, iuf=False, implicit=implicit)
    # item_cf.item_similarity_jaccard(train, norm=True, iuf=False, implicit=implicit)
    # item_cf.item_similarity_jaccard(train, norm=False, iuf=True, implicit=implicit)
    # item_cf.item_similarity_pearson(train, norm=False, iuf=False, implicit=False)
    # item_cf.item_similarity_pearson(train, norm=True, iuf=False, implicit=False)
    # item_cf.item_similarity_pearson(train, norm=False, iuf=True, implicit=False)
    # item_cf.item_similarity_adjusted_cosine(train, norm=False, iuf=False, implicit=False)
    # item_cf.item_similarity_adjusted_cosine(train, norm=True, iuf=False, implicit=False)
    # item_cf.item_similarity_adjusted_cosine(train, norm=False, iuf=True, implicit=False)
    # item_cf.item_similarity_log_likelihood(train, norm=False, implicit=True)
    # item_cf.item_similarity_log_likelihood(train, norm=True, implicit=True)
    # slope_one.item_deviation(train, implicit=False)
    # lfm.factorization(train, bias=True, svd=False, svd_pp=False, steps=50)  # explicit
    # lfm.factorization(train, bias=False, svd=True, svd_pp=False, steps=50)  # explicit
    # lfm.factorization(train, bias=True, svd=True, svd_pp=False, steps=25)  # explicit
    # lfm.factorization(train, bias=True, svd=True, svd_pp=True, steps=10, gamma=0.03)  # explicit
    # lfm.factorization(train, bias=True, svd=True, svd_pp=False, steps=25, gamma=0.02, slow_rate=0.9, Lambda=0.01,
    #                   ratio=7)  # implicit
    # lfm.factorization(train, bias=True, svd=True, svd_pp=True, steps=50, gamma=0.06, slow_rate=0.95, Lambda=0.01,
    #                   ratio=7)  # implicit

def get_recommendation_explicit(user):
    return user_cf.recommend_explicit(user)
    # return item_cf.recommend_explicit(user)
    # return slope_one.recommend_explicit(user)
    # return lfm.recommend_explicit(user)


def get_recommendation_implicit(user):
    return user_cf.recommend_implicit(user, _n, _user_k)
    # return item_cf.recommend_implicit(user, _n, _item_k)
    # return lfm.recommend_implicit(user, _n)


"""
对用户u推荐n个物品，记为R(u)
令用户u在测试集上喜欢的物品集合为T(u)
"""


def recall():
    """
    召回率描述有多少比例的用户-物品评分记录包含在最终的推荐列表中
    Recall = ∑|R(u) ∩ T(u)| / ∑|T(u)|
    :return: 召回率
    """
    hit = 0
    count = 0
    for user in train.iterkeys():
        tu = test.get(user, {})
        rank = get_recommendation_implicit(user)
        for item, pui in rank:
            if item in tu:
                hit += 1
        count += len(tu)
    return hit / count


def precision():
    """
    准确率描述最终的推荐列表中有多少比例是发生过的用户-物品评分记录
    Precision = ∑|R(u) ∩ T(u)| / ∑|R(u)|
    :return: 准确率
    """
    hit = 0
    count = 0
    for user in train.iterkeys():
        tu = test.get(user, {})
        rank = get_recommendation_implicit(user)
        for item, pui in rank:
            if item in tu:
                hit += 1
        count += len(rank)
    return hit / count


def coverage():
    """
    该覆盖率表示最终的推荐列表中包含多大比例的物品
    Coverage = U|R(u)| / |I|
    覆盖率反映了推荐算法发掘长尾的能力，覆盖率越高，说明推荐算法越能够将长尾中的物品推荐给用户
    :return: 覆盖率
    """
    recommend_items = set()
    all_items = set()
    for user in train.iterkeys():
        for item in train[user].iterkeys():
            all_items.add(item)
        rank = get_recommendation_implicit(user)
        for item, pui in rank:
            recommend_items.add(item)
    return len(recommend_items) / len(all_items)


def popularity():
    """
    这里用推荐列表中物品的平均流行度度量推荐结果的新颖度
    如果推荐出的物品都很热门，说明推荐的新颖度较低，否则说明推荐结果比较新颖
    计算平均流行度时对每个物品的流行度取对数，这是因为物品的流行度分布满足长尾分布，在取对数后，流行度的平均值更加稳定
    :return: 平均流行度
    """
    item_popularity = {}
    for items in train.itervalues():
        for item in items.iterkeys():
            item_popularity.setdefault(item, 0)
            item_popularity[item] += 1
    popularity_sum = 0
    count = 0
    for user in train.iterkeys():
        rank = get_recommendation_implicit(user)
        for item, pui in rank:
            popularity_sum += math.log(1 + item_popularity[item])
        count += len(rank)
    return popularity_sum / count


def RMSE():
    """
    :return: 均方根误差
    """
    rmse_sum = 0
    hit = 0
    for user in train.iterkeys():
        tu = test.get(user, {})
        rank = get_recommendation_implicit(user)
        for item, pui in rank:
            if item in tu:
                rmse_sum += (tu[item] - pui) ** 2
                hit += 1
    return math.sqrt(rmse_sum / hit)


def MAE():
    """
    :return: 平均绝对误差
    """
    mae_sum = 0
    hit = 0
    for user in train.iterkeys():
        tu = test.get(user, {})
        rank = get_recommendation_implicit(user)
        for item, pui in rank:
            if item in tu:
                mae_sum += abs(tu[item] - pui)
                hit += 1
    return mae_sum / hit


# def MAP():
#     """
#     :return: 平均准确率
#     """
#     map_sum = 0
#     for user in train.iterkeys():
#         hit = 0
#         count = 0
#         tu = test.get(user, {})
#         rank = get_recommendation(user)
#         for index, item in enumerate(rank):
#             if item[0] in tu:
#                 hit += 1
#                 count += hit / (index + 1)
#         map_sum += count / len(rank)
#     return map_sum / len(train)


def evaluate_explicit():
    hit = 0
    rmse_sum = 0
    mae_sum = 0
    for user in train.iterkeys():
        tu = test.get(user, {})
        rank = get_recommendation_explicit(user)
        for item, pui in rank:
            if item in tu:
                hit += 1
                rmse_sum += (tu[item] - pui) ** 2
                mae_sum += abs(tu[item] - pui)
    rmse_value = math.sqrt(rmse_sum / hit)
    mae_value = mae_sum / hit
    return rmse_value, mae_value


def evaluate_implicit():
    item_popularity = {}
    for items in train.itervalues():
        for item in items.iterkeys():
            item_popularity.setdefault(item, 0)
            item_popularity[item] += 1
    hit = 0
    test_count = 0
    recommend_count = 0
    recommend_items = set()
    all_items = set()
    popularity_sum = 0
    for user in train.iterkeys():
        tu = test.get(user, {})
        rank = get_recommendation_implicit(user)
        for item, pui in rank:
            if item in tu:
                hit += 1
            recommend_items.add(item)
            popularity_sum += math.log(1 + item_popularity[item])
        test_count += len(tu)
        recommend_count += len(rank)
        for item in train[user].iterkeys():
            all_items.add(item)
    recall_value = hit / test_count
    precision_value = hit / recommend_count
    coverage_value = len(recommend_items) / len(all_items)
    popularity_value = popularity_sum / recommend_count
    return recall_value, precision_value, coverage_value, popularity_value
