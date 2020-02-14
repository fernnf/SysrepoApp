import sysrepo as sr


def module_change_cb(sess, module_name, xpath, event, request_id, private_data):
    print(xpath)

    return sr.SR_ERR_OK


def print_current_config(session, module_name):
    select_xpath = "/" + module_name + ":*//."

    values = session.get_items(select_xpath)

    for i in range(values.val_cnt()):
        print(values.val(i).to_string(), end='')


if __name__ == '__main__':
    try:
        module_name = "sdnmultilayer-app"
        conn = sr.Connection(sr.SR_CONN_DEFAULT)
        sess = sr.Session(conn)
        subscribe = sr.Subscribe(sess)
        subscribe.module_change_subscribe(module_name,module_change_cb, None, None, 0, sr.SR_SUBSCR_DONE_ONLY)

        try:
            print_current_config(sess, module_name)
        except Exception as e:
            pass

        sr.global_loop()

        subscribe.unsubscribe()
        sess.session_stop()
        conn = None

        print("Application exit requested, exiting.\n")

    except Exception as e:

        print(e)
