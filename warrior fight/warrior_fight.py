import random
import time

class Warrior():
#set the Warrior's name,heath,attckmax,blockmax
	def __init__(self,name,health,attackmax,blockmax):
		self.Name=name
		self.Health=health
		self.AttackMax=attackmax
		self.BlockMax=blockmax
	
	def show(self):
		print("the Warrior's name : %s, health : %d, attack : %oblock : %d" \
			%(self.Name,self.Health,self.AttackMax,self.BlockMax))

	def attack(self):
		return random.randint(0,self.AttackMax)
	def block(self):
		return random.randint(0,self.BlockMax)


class Battle():
	def __init__(self):
		self.game_round=1
#game action
	def fight(self,Warrior1,Warrior2):
		while True:
			if self.Get_battleresult(Warrior1,Warrior2)=="Game Over":
				print("game round is :%d Game Over,the winner is %s, the loser is %s"%(self.game_round, \
					Warrior1.Name,Warrior2.Name))
				break
			elif self.Get_battleresult(Warrior2,Warrior1)=="Game Over":
				print("game round is :%d Game Over,the winner is %s, the loser is %s"%(self.game_round, \
					Warrior2.Name,Warrior1.Name))
				break

	def Get_battleresult(self,WarriorA,WarriorB):
		damage=WarriorA.attack() - WarriorB.block()
		if damage< 0:
			damage=0
		WarriorB.Health = WarriorB.Health - damage
		print("round :%d,%s is attack %s, %s \'s health is %d"%(self.game_round,WarriorA.Name,WarriorB.Name,WarriorB.Name, \
			WarriorB.Health))
		self.game_round+=1
		if WarriorB.Health<=0:
			return "Game Over"

	

if __name__ == '__main__':
	WarriorA=Warrior("John",100,30,20)
	WarriorB=Warrior("Mike",100,25,25)
	battle=Battle()
	battle.fight(WarriorA,WarriorB)