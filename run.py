import startLogin
import test

def main():
    validity = False
    validity = startLogin.main()
    print("Got This Far")
    print(validity)
    if validity == True:
        print(test)
    
if __name__ == "__main__":
    main()