except:
    act = ActionChains(driver)
    act.send_keys(Keys.PAGE_DOWN).perform()
    i = i - 1