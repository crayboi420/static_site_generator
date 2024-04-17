from textnode import TextNode

def main():
    n1 = TextNode("Hello","pdf","www.google.com")
    n2 = TextNode("Hello","pdf","www.google.com")
    n3 = TextNode("Hello hi","pdf","www.google.com")
    print(n1, n1==n2, n1 == n3)

if __name__=='__main__':
    main()