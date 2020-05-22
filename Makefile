all:
		cp trade.py trade
		chmod +x trade
clean:

fclean:	clean
		rm trade

re:		fclean all