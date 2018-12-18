import evaluator
import card
import os
if __name__ == "__main__":


	diler = card.Dealer()
	a = card.Hand("Justynka",card.Card("n","n"),card.Card("n","n"))
	b = card.Hand("Seba    ",card.Card("n","n"),card.Card("n","n"))
	c = card.Hand("Mateusz ",card.Card("n","n"),card.Card("n","n"))
	d = card.Hand("Szymek  ",card.Card("n","n"),card.Card("n","n"))
	f = card.Hand("Melwin  ",card.Card("n","n"),card.Card("n","n"))
	
	imiona = []

	for p in [a,b,c,d,f]:
		imiona.append(p.getName())
	wyniki = [0,0,0,0,0]
	e = evaluator.Evaluator()

	while True:
		os.system("cls")
		diler.deal(a,b,c,d,f)

		diler.performFlop()
		diler.performTurn()
		diler.performRiver()
		t = diler.getTable()
		
		print "-------------------------------------------------------------------------------\nNA STOLE:  >>>>>>>>>>",diler.showTable(),"<<<<<<<<<<<<<<<\n-------------------------------------------------------------------------------"
		
		for p in (a,b,c,d,f):
			e.eval(p,t)

		gracze = e.ranking(a,b,c,d,f)

		rankingi = []
		for p in [a,b,c,d,f]:
			print p.getName(), p.showHand(), ">>>>>", p.handInfo(), "\n"
		for p in gracze:			
			rankingi.append(p.getRank())

		ile = rankingi.count(gracze[0].getRank())
		print "Wygrywa:"
		for i in range(ile):
			imie = gracze[i].getName()
			print imie

		raw_input()
