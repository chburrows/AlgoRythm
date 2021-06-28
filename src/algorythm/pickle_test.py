from settings import Settings

if __name__ == '__main__':
    #testobj = Settings(0, 7, 25, 15, 150, 2, 64, (255, 255, 255), 48, 32, (255, 255, 255))
    testobj = Settings(1, 2, 3, 4, 5, 6, 7, (0, 1, 2), 50, 60, (99, 99, 99))

    testobj.save('saved_preferences2')
    #testobj.load('saved_preferences2')

    print(testobj.b_color, testobj.text_color)