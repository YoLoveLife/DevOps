class One():
    def __init__(self):
        self.ddr = 1

    def get_ddr(self):
        print(self.ddr)



class Two():
    def __init__(self):
        self.test=One()

    def set_one(self,test):
        self.test=test

    def one_add(self):
        self.test.ddr=5
if __name__ == "__main__":
    # t=One()
    # o=Two()
    # o.set_test(t)
    # o.test_add()
    # t.get_ddr()
    o = One()
    t = Two()
    t.set_one(o)
    t.one_add()
    o.get_ddr()