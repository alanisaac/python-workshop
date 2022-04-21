class A:
    def do_thing(self):
        print('From A')


class B(A):
    def do_thing(self):
        print('From B')


class C(A):
    def do_thing(self):
        print('From C')


class D(B, C):
    pass


d = D()
d.do_thing()
