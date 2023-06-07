"""
训练并评估单一模型的脚本
"""

import argparse
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '3'
from libcity.pipeline import run_model
from libcity.utils import str2bool, add_general_args
import random
import pandas as pd
import numpy as np

log = './log/'

if __name__ == '__main__':
    total = 5
    for i in range(total):
        seed = random.randint(0, 10000)

        parser = argparse.ArgumentParser()
        # 增加指定的参数
        parser.add_argument('--task', type=str,
                            default='traffic_state_pred', help='the name of task')
        parser.add_argument('--model', type=str,
                            default='RNN', help='the name of model')
        parser.add_argument('--dataset', type=str,
                            default='CHITaxi20190406', help='the name of dataset')
        parser.add_argument('--config_file', type=str,
                            default=None, help='the file name of config file')
        parser.add_argument('--saved_model', type=str2bool,
                            default=True, help='whether save the trained model')
        parser.add_argument('--train', type=str2bool, default=True,
                            help='whether re-train model if the model is trained before')
        parser.add_argument('--exp_id', type=str, default=None, help='id of experiment')
        parser.add_argument('--seed', type=int, default=seed, help='random seed')
        # 增加其他可选的参数
        add_general_args(parser)
        # 解析参数
        args = parser.parse_args()
        dict_args = vars(args)
        other_args = {key: val for key, val in dict_args.items() if key not in [
            'task', 'model', 'dataset', 'config_file', 'saved_model', 'train'] and
            val is not None}
        run_model(task=args.task, model_name=args.model, dataset_name=args.dataset,
                  config_file=args.config_file, saved_model=args.saved_model,
                  train=args.train, other_args=other_args)

    save_path = log + args.dataset[0:3] + '/' + args.model + '_' + args.dataset +'/'

    result_csv = os.listdir(save_path)
    final_results_ten_train = np.zeros([12, 4, 5])
    for i in range(len(result_csv)):
        result = pd.read_csv(save_path + result_csv[i])
        temp = result[["MAE", "RMSE", 'micro-F1', 'macro-F1']].values
        final_results_ten_train[:, :, i] = temp

    avg_results = np.zeros([12, 4])
    arr_results = np.zeros([12, 4])
    ## 计算 指标均值 和方差
    for j in range(final_results_ten_train.shape[0]):
        avg_mae_rmse_microf1_macrof1 = np.mean(final_results_ten_train[j, :, :], axis=1)
        arr_mae = np.var(final_results_ten_train[j, :, :][0])
        arr_rmse = np.var(final_results_ten_train[j, :, :][1])
        arr_microf1 = np.var(final_results_ten_train[j, :, :][2])
        arr_macrof1 = np.var(final_results_ten_train[j, :, :][3])


        avg_results[j] = avg_mae_rmse_microf1_macrof1
        arr_results[j][0] = arr_mae
        arr_results[j][1] = arr_rmse
        arr_results[j][2] = arr_microf1
        arr_results[j][3] = arr_macrof1

    np.savetxt(save_path + 'avg_result.csv', avg_results)
    np.savetxt(save_path + 'arr_result.csv', arr_results)