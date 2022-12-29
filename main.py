from base.create import Create
from base.model import Model
from base.process import Process
from bank.Bank_Create import CreateBank
from bank.Bank_model import Bank_model
from bank.Bank_Process import Bank_Process
from base import fun_rand
from hospital.create_hospital import Create_hospital
from hospital.dispose_hospital import Dispose_hospital
from hospital.model_hospital import Model_hospital
from hospital.process_hospital import Process_hospital

def base_model(p1):
    c1 = Create(delay_mean=5, name='CREATOR', distribution='exp')
    p2 = Process(max_queue=3, delay_mean=5, distribution='exp')
    p3 = Process(max_queue=3, delay_mean=5, distribution='exp')

    c1.next_element = [p1]
    p1.next_element = [p2, p3]
    elements = [c1, p1, p2, p3]
    model = Model(elements)
    model.simulate(1000)

def priority_model():
    print('Priority model')
    p1 = Process(max_queue=3, delay_mean=5, distribution='exp')
    p1.priority = [2, 1]

    base_model(p1)

def probability_model():
    print('Probability model')
    p1 = Process(max_queue=3, delay_mean=5, distribution='exp')

    p1.probability = [0.9, 0.1]
    base_model(p1)

def bank_model():
    print('Bank model')
    c1 = CreateBank(delay_mean=0.5, name='CREATOR', distribution='exp')
    p1 = Bank_Process(max_queue=3, delay_mean=0.3, name='CASHIER_1', distribution='exp')
    p2 = Bank_Process(max_queue=3, delay_mean=0.3, name='CASHIER_2', distribution='exp')

    c1.next_element = [p1, p2]

    p1.state[0] = 1
    p2.state[0] = 1

    p1.t_next[0] = fun_rand.norm(1, 0.3)
    p2.t_next[0] = fun_rand.norm(1, 0.3)

    c1.t_next[0] = 0.1

    p1.queue = 2
    p2.queue = 2

    element_list = [c1, p1, p2]
    bank = Bank_model(element_list, balancing=[p1, p2])
    bank.simulate(1000)

def hospital_model():
    print('Hospital model')
    c1 = Create_hospital(delay_mean=15.0, name='CREATOR_1', distribution='exp')
    p1 = Process_hospital(max_queue=100, n_channel=2, name='RECEPTION', distribution='exp')
    p2 = Process_hospital(max_queue=100, delay_mean=3.0, delay_dev=8, n_channel=3, name='FOLLOWING_TO_THE_WARD',
                         distribution='unif')
    p3 = Process_hospital(max_queue=0, delay_mean=2.0, delay_dev=5, n_channel=10, name='FOLLOWING_TO_THE_LAB_RECEPTION',
                         distribution='unif')
    p4 = Process_hospital(max_queue=100, delay_mean=4.5, delay_dev=3, n_channel=1, name='LAB_REGISTRY',
                         distribution='erlang')
    p5 = Process_hospital(max_queue=100, delay_mean=4.0, delay_dev=2, n_channel=1, name='EXAMINATION',
                         distribution='erlang')
    p6 = Process_hospital(max_queue=0, delay_mean=2.0, delay_dev=5, n_channel=10, name='FOLLOWING_TO_THE_RECEPTION',
                         distribution='unif')

    d1 = Dispose_hospital(name='EXIT1')
    d2 = Dispose_hospital(name='EXIT2')

    c1.next_element = [p1]
    p1.next_element = [p2, p3]
    p2.next_element = [d1]
    p3.next_element = [p4]
    p4.next_element = [p5]
    p5.next_element = [d2, p6]
    p6.next_element = [p1]

    p1.prior_types = [1]

    p1.required_path = [[1], [2, 3]]
    p5.required_path = [[3], [2]]

    elements = [c1, p1, p2, p3, p4, p5, p6, d1, d2]

    model = Model_hospital(elements)
    model.simulate(1000)



hospital_model()