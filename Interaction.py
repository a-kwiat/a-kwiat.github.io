from ClassUtil import CustomCopy

class InteractionLogic:
	def __call__(self, *objects, data=None):
		raise NotImplementedError()

# class BasicInteraction(InteractionLogic):
# 	pass

# class SelfInteraction(InteractionLogic):
# 	def __init__(self, *, name):
# 		self.name = name

class DofInteraction():
	def __init__(self, *, name, logic):
		self.name = name
		self.interaction_logic = logic

	def perform(self, *, entity, **data):
		self.interaction_logic(entity=entity, **data)
	# def __call__(self, *, entity, data=None):
	# 	self.interaction_logic()
		# raise NotImplementedError()


# class SinglePassInteraction():
# 	pass
# @QuickClone("bound_dof", pDict={"action":"actions"})
# @CustomCopy(actions=lambda actions: actions[:])
class Interaction:
	def __init__(self, *, name, action, selector=None, tag=None):
		self.name = name
		self.actions = [action]
		self.selector = selector
		self.tag = tag

		self.bound_dof = None
		self.world = None

		# self.__class__ = InteractionLogic

	def perform(self, *args, **kwargs):
		# print("performing: ", self.name)
		if self.selector is None:
			# print(args)
			for a in self.actions:
				if self.bound_dof:
					# print("args: ", args)
					a(self.bound_dof, *args, **kwargs)
				else:
					a(*args, **kwargs)
			# self.action(*args, **kwargs)
		else:
			raise NotImplementedError

	def initialize(self, world):
		self.world = world

	def __copy__(self):
		ret = type(self)(name=self.name, action=None, selector=self.selector, tag=self.tag)
		ret.actions = self.actions[:]
		ret.bound_dof = self.bound_dof
		ret.world = self.world
		return ret
		# ret = copy.copy(self)
		# ret.actions = self.actions[:]

	@property
	def action(self):
		return self.actions[0]


	def add_action(self, action):
		self.actions.append(action)

	def bind_to_dof(self, dof):
		self.bound_dof = dof

if __name__ == "__main__":
	import copy

	i = Interaction(name='n', action=lambda x: print("action", x), tag="tag")
	print(type(i))

	i2 = Interaction(name='o', action=lambda x: print("action2", x), tag="tagg2")
	# i.__class__ = InteractionLogic
	# i2 = i.clone()
	# print(vars(i2))


	i3 = copy.copy(i)
	print(type(i3))
	i3.actions.append(4)
	print("copy: ", vars(i3))
	print("orig: ", vars(i))

	# def perform(self, *entities, **data):
	# 	self.interaction_logic(*entities, **data)

	# def targets(dof):
	# 	if not self.selector:
	# 		yield dof
	# 		return
	# 	else:
	# 		for d in dof.items():
	# 			if (self.selector(d)):
	# 				yield d
	# 		return

	# def perform(self, dof):
	# 	for t in self.targets(dof):
	# 		self.interaction_logic(t)

	# def interaction_logic(target):
	# 	# actually do stuff here
	# 	# intended for subclass override (think carefully about how)
	# 	pass


	# def gather_targets(self, *, gather_fn):
	# 	self.target_lists = {tname:gather_fn(tname) for tname in self.target_names}

	# @classmethod
	# def Build(name, logic=None, selector=None, filter=None):
	# 	ret = Interaction(name)
	# 	ret.selector = selector
	# 	ret.filter = filter
		

		
class InteractionManager:

	def __init__(self):
		pass
		# mix-ee:
			# self.interactions = [] # list of (name, [target_name], interaction)


	def register_interaction(*, name, interaction, target_names):
		interaction = Interaction(name=name, interaction_logic=interaction_logic, target_names=target_names)
		interaction.gather_targets(gather_fn=self.gather_interaction_target)
		self.interactions.add(interaction)

	def perform_interaction(self, interaction, *args, **kwargs):
		# for interaction_details in self.interactions:
			# interaction = interaction_details.interaction

		# tnames = interaction.target_names
		targets = interaction.target_lists

		if len(targets) == 1:
			pc = targets[0]
			for particle in pc:
				interaction.interaction_logic(particle, **kwargs)
		elif len(targets) == 2:
			pc1 = targets[0]
			pc2 = targets[1]

			for p1 in pc1:
				for p2 in pc2:
					if interaction.selects(p1, p2):
						interaction.act(p1, p2)
					# interaction.interaction_logic(pc1, pc2, **kwargs)
		else:
			raise ValueError("bad number of targets in interaction: {}".format(interaction.name))

	def gather_interaction_target(tname):
		raise NotImplementedError("should be implemented by mix-ee")


class TypeInteraction(Interaction):
	def __init__(self, *, name, logic, particles):
		super().__init__(name=name, logic=logic, targets=particles)

class SelfCollision(InteractionLogic):
	def __call__(self, *objects, **kwargs):
		assert len(objects) == 2
		p1 = objects[0]
		p2 = objects[1]

		if p1.position == p2.position:
			raise BaseException("collided")




