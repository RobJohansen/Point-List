from mechanize import Browser
from bs4 import BeautifulSoup
import logging

def new_browser():
    b = Browser()

    b.set_handle_robots(False)
    b.set_handle_refresh(False)
    b.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    
    return b


def get_points_bw(self, m, rs):
    try:
        # BROWSE
        b = new_browser()
        b.open(m.scheme.page)

        b.form = list(b.forms())[0]
        b[m.scheme.form_user] = m.username
        b[m.scheme.form_pass] = m.password
        b.submit()
        
        html = b.open('/mt/www.bestwestern.com/rewards/').read()
        b.close()

        # TRAVERSE
        soup = BeautifulSoup(html).find(id=m.scheme.match)

        rs['content'] = soup.findChildren()[1]
        rs['points'] = rs['content'].div('div')[1].contents[1][2:]
        rs['success'] = True

    except Exception, e:
        logging.info(e)
        rs['success'] = False

    finally:
        b.close()

    return rs


def get_points_ba(self, m, rs):
    try:
        # BROWSE
        b = new_browser()
        b.open(m.scheme.page)

        b.select_form(name=m.scheme.form_name)
        b[m.scheme.form_user] = m.username
        b[m.scheme.form_pass] = m.password
       
        html = b.submit().read()
        b.close()

        # TRAVERSE
        soup = BeautifulSoup(html).find(id=m.scheme.match)

        rs['content'] = soup
        rs['points'] = rs['content'].findAll('span', { 'class' : 'nowrap' })[0].string[10:-2]
        rs['success'] = True

    except Exception, e:
        logging.info(e)
        rs['success'] = False

    finally:
        b.close()

    return rs


# def get_points_hh(self, m):
#     # BROWSE
#     b = new_browser()
#     b.open(m.scheme.page)

#     b.select_form(name=m.scheme.form_name)
#     b[m.scheme.form_user] = m.username
#     b[m.scheme.form_pass] = m.password
   
#     html = b.submit().read()
#     b.close()

#     # TRAVERSE
#     soup = BeautifulSoup(html).find(id=m.scheme.match)
    
#     return {
#         'content'   : soup,
#         'points'    : soup.find(id='my_account_grid_top_middle').h2.strong.string,
#         'status'    : ''
#     }


# def get_points_sb(self, m, rs):
#     try:
#         # BROWSE
#         b = new_browser()
#         b.open(m.scheme.page)

#         b.form = list(b.forms())[0]
#         b[m.scheme.form_user] = m.username
#         b[m.scheme.form_pass] = m.password
        
#         html = b.submit().read()

#         # TRAVERSE
#         soup = BeautifulSoup(html).find(id=m.scheme.match)

#         rs['content'] = soup
#         rs['points'] = ''
#         rs['status'] = 'Success'

#     except Exception, e:
#         rs['status'] = 'Error'

#     finally:
#         b.close()

#     return rs


# def get_points_co(self, m):
#     # BROWSE
#     b = new_browser()
#     b.open(m.scheme.page)

#     b.select_form(name=m.scheme.form_name)
#     b[m.scheme.form_user] = m.username
#     b[m.scheme.form_pass] = m.password
    
#     html = b.submit().read()
#     b.close()

#     # TRAVERSE
#     soup = BeautifulSoup(html).find(id=m.scheme.match)
    
#     return {
#         'content'   : soup,
#         'points'    : soup.find(id='txtCounterValueHeader').value.strip(),
#         'status'    : ''
#     }


# def get_points_ma(self, m):
#     # BROWSE
#     b = new_browser()
#     b.open(m.scheme.page)

#     b.select_form(name=m.scheme.form_name)
#     b[m.scheme.form_user] = m.username
#     b[m.scheme.form_pass] = m.password
#     b.submit()

#     self.response.write(b.response().read())

#     b.follow_link(text_regex='Home')

#     html = b.response().read()
#     b.close()

#     # TRAVERSE
#     soup = BeautifulSoup(html).find(id=m.scheme.match)

#     return {
#         'content'   : soup,
#         'points'    : 'Not Implemented', #content.find(id='my_account_grid_top_middle').h2.strong.string.strip()
#         'status'    : ''
#     }


def get_unknown(self, m, rs):
    rs['status'] = False
    
    return rs


def updater(self, m):    
    # xs = {
    #     'Hilton HHonors'    : get_points_hh,
    #     'Starbucks'         : get_points_sb,
    #     'Costa'             : get_points_co,
    #     'Marriott Rewards'  : get_points_ma
    # }

    rs = {
        'content'   : '',
        'points'    : '',
        'status'    : ''
    }

    xs = {
        'Best Western'      : get_points_bw,
        'British Airways'   : get_points_ba,
    }

    f = xs.get(m.scheme.get().name, get_unknown)

    return f(self, m, rs)