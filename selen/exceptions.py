class EmptyInbox(Exception):
	pass

class CantGoFurther(Exception):
	pass

class CantLogin(CantGoFurther):
	pass