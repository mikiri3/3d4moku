#!/usr/bin/python3
# -*- coding: utf-8 -*-
#3d4moku_2のguiを作りたい
#3d表示をすることになりました．
#ボタンを配置はできてない
#3dが重い

#欲しいもの↓
#どちらの手番か表示
#置けないところには置けない
#勝敗判定
#文字じゃなくてわかりやすい表示
#一手戻るなど，リセット


from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QGridLayout, QPushButton,
	QLabel, QApplication)
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

import sys
import os
import time


class Board():
	def __init__(self):
		super().__init__()

	def show(self, x, y, z, player):
		plt.close()
		"""
		#軸を同時に表示しようとしたけど面倒そうなのでやめた
		axis_x = [ 0 ]
		axis_y = [ 0 ]
		axis_z = np.array([[0], [4]])
		#axis_z = np.arange(0.0 , 3.0, 1.0)
		print(axis_z)
		fig_2 = plt.figure(1)
		ax_2 = Axes3D(fig_2)
		ax_2.plot_wireframe(axis_x, axis_y, axis_z)
		#plt.show()"""



		fig = plt.figure(1)
		ax = fig.gca( projection='3d' )

		#ax = fig.add_subplot(111, projection='3d') #行数列数なんばん目のプロットか...?

		ax.scatter(x[0], y[0], z[0], "o", c="red", s=100)
		ax.scatter(x[1], y[1], z[1], "o", c="black", s=100)
		#player 1 なら赤
		#if player == 1:
		#	ax.scatter(x, y, z, "o", c="red", s=100)
		#else: ax.scatter(x, y, z, "o", c="black", s=100)


		#棒の部分を表示したい
		for i in range(4):
			for j in range(4):

				a = [ i, i ]
				b = [ j, j ]
				c = [-1, 4]

				ax.plot(a, b, c, color = 'gray')
		#plt.axhline(x=2, lw=2, color='red')
		#plt.plot(x, z, label='test',linewidth=3,color='b', marker='^',markeredgecolor="black")





		#表示範囲の指定
		ax.set_xlim(-1, 4)
		ax.set_ylim(-1, 4)
		ax.set_zlim(-1, 4)


		# 一番のポイント
		# - plt.show() ブロッキングされてリアルタイムに描写できない
		# - plt.ion() + plt.draw() グラフウインドウが固まってプログラムが止まるから使えない
		# ----> plt.pause(interval) これを使う!!! 引数はsleep時間
		plt.pause(3)
		#plt.show()

	def makeList(self, field, player): #数字ごとに3d表示のためのリストを作る
		x_1 = []
		y_1 = []
		z_1 = []
		for i in range(4):
			for j in range(4):
				for k in range(4):
					if field[k][i][j] == 1:
						x_1.append(i)
						y_1.append(j)
						z_1.append(3 - k)

		#プレイヤー2の石
		x_2 = []
		y_2 = []
		z_2 = []
		for i in range(4):
			for j in range(4):
				for k in range(4):
					if field[k][i][j] == 2:
						x_2.append(i)
						y_2.append(j)
						z_2.append(3 - k)
		#print('yeah'+str(x))
		#print('yeah'+str(y))
		#print('yeah'+str(z))

		self.show((x_1, x_2), (y_1, y_2), (z_1, z_2), player)


class Game():

	def __init__(self):
		super().__init__()
		#field [k段目][i行目][j列目]が1ならプレイヤー1の石がある
		self.field = [[[ 0 for k in range(4)] for i in range(4)] for j in range(4)]

		self.player = 1

		self.board = Board()

	def show(self): #表示する
		#sys.stdout.write('\r\r\r\r\033[K')
		print("\x1b[2J\x1b[0;0H" , end = "")
		for k in range(4):
			sys.stdout.write(str(4-k) + '段目\n')
			sys.stdout.flush()
			for i in range(4):
				sys.stdout.write(str(self.field[k][i]) + '\n')
				sys.stdout.flush()
			#sys.stdout.write('\r\r\r\r\033[K' )
			#sys.stdout.flush()


		#sys.stdout.write("\r")

	def isAble(self, place):
		#0~3の範囲外ならFalse
		if place[0] > 3 or place[1] > 3:
			print("置けない")
			return False

		#すでに「4段目まで」置いてあったらFalse
		if self.field[0][int(place[0])] [int(place[1])] != 0:
			print("置けない")
			return False
		print("置ける")
		return True

	def put(self):#石をうつ&勝敗ついたらTrueを返す
		#print('x y: ')
		while(1):
			print("プレイヤー" + str(self.player) + "の番です")
			input_line = input('x y: ').rstrip().split()
			try:
				place = []
				place.append(int(input_line[0]))
				place.append(int(input_line[1]))
			except: #エラーが起きたらもう一度
				print('ちゃんと入力して')
				continue
			else: #起きなければ置けるか判定していく
				#置けるかどうか
				if self.isAble(place):
					break
				else: continue


		#置ける一番低い段に置く
		for i in reversed(range(4)):
			print(i)
			if self.field[i][place[0]] [place[1]] != 0: #その段が埋まっていたら次の段を見る，置けるか判定と重複してる感ある
				continue
			else:
				self.field[i][place[0]] [place[1]] = self.player
				break

		self.show() #コンソールに表示する

		#グラフで書く↓
		self.board.makeList(self.field, self.player)

		if self.isWin(place, i):
			print(str(self.player) + 'の勝ち')
			quit = int(input('"1"と入力すると終了: '))
			if quit ==1:
				return True

		self.player = 3 - self.player
		return False

	def isWin(self, place, height): #置いた位置を引数として，勝利判定をする

		print(str(4 - height) + "段目" , place)

		#height段-------------------------------------------------------------------------
		#前後
		flag = 1 #最後まで1なら4連
		for i in range(4):
			if self.field[height][ i ][place[1]] != self.player:
				flag = 0
				break
		if flag == 1:
			return True

		#左右でなるか
		flag = 1
		for j in range(4):
			if self.field[height][place[0]][ j ] != self.player:
				flag = 0
				break
		if flag == 1:
			return True

		#同じ段斜め左上から
		flag = 1
		for i in range(4):
			if self.field[height][ i ][ i ] != self.player:
				flag = 0
				break
		if flag == 1:
			return True

		#同じ段斜め右上から
		flag = 1
		for i in range(4):
			if self.field[height][ i ][ 3 - i ] != self.player:
				flag = 0
				break
		if flag == 1:
			return True

		#place[0] 行-------------------------------------------------------------------------
		#上下
		flag = 1 #最後まで1なら4連
		for k in range(4):
			if self.field[k][place[0]][place[1]] != self.player:
				flag = 0
				break
		if flag == 1:
			return True

		#左右でなるか
		flag = 1
		for j in range(4):
			if self.field[height][place[0]][ j ] != self.player:
				flag = 0
				break
		if flag == 1:
			return True

		#同じ段斜め左上から
		flag = 1
		for i in range(4):
			if self.field[ i ][place[0]][ i ] != self.player:
				flag = 0
				break
		if flag == 1:
			return True

		#同じ段斜め右上から
		flag = 1
		for i in range(4):
			if self.field[ i ][place[0]][ 3 - i ] != self.player:
				flag = 0
				break
		if flag == 1:
			return True


		#place[1] 列-------------------------------------------------------------------------
		#上下
		flag = 1 #最後まで1なら4連
		for k in range(4):
			if self.field[k][place[0]][place[1]] != self.player:
				flag = 0
				break
		if flag == 1:
			return True

		#前後でなるか
		flag = 1
		for i in range(4):
			if self.field[height][ i ][place[1]] != self.player:
				flag = 0
				break
		if flag == 1:
			return True

		#同じ段斜め左上から
		flag = 1
		for i in range(4):
			if self.field[ i ][ i ][place[1]] != self.player:
				flag = 0
				break
		if flag == 1:
			return True

		#同じ段斜め右上から
		flag = 1
		for i in range(4):
			if self.field[ i ][ 3 - i ][place[1]] != self.player:
				flag = 0
				break
		if flag == 1:
			return True


		#例外対角線1
		flag = 1
		for i in range(4):
			if self.field[ i ][ i ][ i ] != self.player:
				flag = 0
				break
		if flag == 1:
			return True

		#例外対角線2
		flag = 1
		for i in range(4):
			if self.field[ 3 - i ][ i ][ i ] != self.player:
				flag = 0
				break
		if flag == 1:
			return True

		#例外対角線3
		flag = 1
		for i in range(4):
			if self.field[ i ][ 3 - i ][ i ] != self.player:
				flag = 0
				break
		if flag == 1:
			return True

		#例外対角線4
		flag = 1
		for i in range(4):
			if self.field[ 3 - i ][ 3 - i ][ i ] != self.player:
				flag = 0
				break
		if flag == 1:
			return True

		return False

if __name__ == '__main__':
	game = Game()
	game.show()
	#player = 1
	while(1):
		if game.put():
			break
		#game.show()
		#player = 3 - player
