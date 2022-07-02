from app import bp
@bp.route('/health-check', methods=(['GET']))
def health_check():
    return 'page ok!'