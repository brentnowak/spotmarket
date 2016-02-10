#-----------------------------------------------------------------------------
# spotmarket_flask.py - EVE Online Market Evaluator
# https://github.com/brentnowak/spotmarket
# Brent Nowak <brent613@gmail.com>
#-----------------------------------------------------------------------------
# Version: 0.1
# - Initial release
# Version: 0.3
# - Migration to Flask+Bootstrap
#-----------------------------------------------------------------------------

from app import app

app.run(host='0.0.0.0', port=80, debug=True, threaded=True)