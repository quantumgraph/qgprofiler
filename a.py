from qgprofiler import QGProfiler
import time

def g(qgp):
    qgp.push('g')
    time.sleep(0.01)
    qgp.pop()
    qgp.push('k1')
    qgp.update('s1', 5)
    qgp.update('m1', 1000)
    qgp.pop()

def f(qgp):
    time.sleep(0.1)
    g(qgp)

if __name__ == '__main__':
    attributes = {'s1': 'sum', 'm1': 'max'}
    qgp = QGProfiler('my-test', 'out.xml', attributes)
    qgp.update('s1', 10)
    qgp.update('m1', 200)

    for i in range(10):
        qgp.push('f')
        qgp.update('s1', i)
        qgp.update('m1', 100 * i)
        f(qgp)
        qgp.pop()

    qgp.end()
    qgp.generate_file()
