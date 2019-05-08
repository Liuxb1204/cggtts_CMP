import sys,getopt,argparse
import math
if __name__=="__main__":
    print("程序开始...")

    # opts,args = getopt.getopt(sys.argv[1:],"a:cd",["b="])
    # for opt,arg in opts:
    #     if opt=="-a":
    #         print(opt+"---"+arg)
    #     elif opt=="--b":
    #         print(opt+"---"+arg)
    #     elif opt=="-c":
    #         print(opt+"---"+arg)
    #     elif opt == "-d":
    #         print(opt+"---" + arg)
    # print(sys.argv)
    # parser = argparse.ArgumentParser()
    # parser.add_argument("name")
    # args = parser.parse_args()
    # print(args)
    # print(args.name)
    # print(sys.argv[0])
    # print(sys.argv[1])
    # print(sys.argv[2])

    ns = 324.8
    # tan_n = -7.32 * math.exp(0.005577 * ns)
    tan_n = -44.79156892
    # nslog = math.log((ns+tan_n)/105)
    nslog = 0.980859364

    h = 0

    R1 = 2162 + 324.8 - 324.8 * h - 22.39578446 + 22.39578446 * h * h
    R1 = 2464.40421554 - 324.8 * h + 22.39578446 * h * h
    R1 = (2.46440421554 - 0.3248 * h + 0.02239578446 * h * h)/299792458


    print(2.46440421554/299792458,"-",0.3248/299792458,"* h +",0.02239578446/299792458,"* h * h")

