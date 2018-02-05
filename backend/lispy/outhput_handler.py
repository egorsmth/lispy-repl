from backend.lispy.core import get_type, is_empty, car, cdr, get_value, def_env, Lambda, Macro, cons, sub_env, get_env, \
    Env

OK_symbol = 'OK'


def show(l, start_of_list=True):
    type = get_type(l)
    new_list = True

    if type == 'ConsList':
        if is_empty(l):
            return '()'
        if get_type(car(l)) != 'ConsList':
            new_list = False
        if start_of_list:
            return "({} {})".format(show(car(l)), show(cdr(l), new_list))
        else:
            return "{} {}".format(show(car(l)), show(cdr(l), False))
    if type == "<class 'str'>":
        return '"{}"'.format(l)
    return get_value(l)


def realize_bin_op(op, l, r):
    result = 0
    if op == '+':
        result = l + r
    elif op == '-':
        result = l - r
    elif op == '*':
        result = l * r
    elif op == '/':
        result = l / r
    elif op == '%':
        result = l % r
    else:
        raise Exception('Wtf is this bin operator???')

    return result


def eval_bin_op(h, l, e):
    if is_empty(l):
        return None
    result = eval_lisp(car(l), e)
    l = cdr(l)
    while not is_empty(l):
        right_operand = eval_lisp(car(l), e)
        result = realize_bin_op(get_value(h), result, right_operand)
        l = cdr(l)
    return result


def realize_pred_op(op, l, r):
    result = False
    if op == '<':
        result = l < r
    elif op == '<=':
        result = l <= r
    elif op == '>':
        result = l >= r
    elif op == '==':
        result = l == r
    elif op == '!=':
        result = l != r
    elif op == 'and':
        result = l and r
    elif op == 'or':
        result = l or r
    else:
        raise Exception('Wtf is this pred operator???')

    return result


def eval_pred_op(h, l, e):
    if is_empty(l):
        return None

    left_operand = eval_lisp(car(l), e)
    l = cdr(l)
    result = True
    while not is_empty(l):
        right_operand = eval_lisp(car(l), e)
        result = result and realize_pred_op(get_value(h), left_operand, right_operand)
        if not result:
            return False
        left_operand = right_operand
        l = cdr(l)
    return True


def eval_cond(l, e):
    while not is_empty(l):
        cond = car(l)
        pred = car(cond)
        res = car(cdr(cond))
        if pred == 'else':
            return eval_lisp(res, e)
        if eval_lisp(pred, e):
            return eval_lisp(res, e)
        l = cdr(l)
    return None


def eval_special_form(h, l, e):
    if is_empty(l):
        return None
    val = get_value(h)
    if val == 'def':
        t = get_type(car(l))
        if t != 'Symbol':
            raise Exception('Cant assign to {}. Symbol required.'.format(t))
        k = get_value(car(l))
        v = eval_lisp(car(cdr(l)), e)
        def_env(e, k, v)
    elif val == 'defn':
        name = car(l)
        args = car(cdr(l))
        body = car(cdr(cdr(l)))
        k = get_value(name)
        lmbd = Lambda(args, body, e)
        def_env(e, k, lmbd)
    elif val == 'lambda':
        args = car(l)
        body = cdr(l)
        return Lambda(args, body, e)
    elif val == 'macro':
        args = car(l)
        body = cdr(l)
        return Macro(args, body)
    elif val == 'if':
        pred = eval_lisp(car(l), e)
        t = car(cdr(l))
        f = car(cdr(cdr(l)))
        if pred:
            return eval_lisp(t, e)
        else:
            return eval_lisp(f, e)
    elif val == 'car':
        h = car(l)
        return eval_lisp(car(eval_lisp(h, e)), e)
    elif val == 'cdr':
        return cdr(eval_lisp(car(l), e))
    elif val == 'cons':
        h = eval_lisp(car(l), e)
        t = eval_lisp(car(cdr(l)), e)
        return cons(h, t)
    elif val == '`':
        return car(l)
    elif val == 'cond':
        return eval_cond(l, e)
    elif val == 'print':
        while not is_empty(l):
            r = eval_lisp(car(l), e)
            print(r)
            l = cdr(l)
        return OK_symbol
    elif val == 'eval':
        a = eval_lisp(car(l), e)
        return eval_lisp(a, e)
    elif val == 'typeof':
        return get_type(car(l))
    return OK_symbol


def eval_lambda(lmbd, args, e):
    se = sub_env(lmbd.env)
    sub_args = lmbd.args
    while not is_empty(sub_args):
        if is_empty(args):
            raise Exception('not enough args!')
        arg = eval_lisp(car(args), e)
        k = eval_lisp(car(sub_args), se)
        def_env(se, k, arg)
        sub_args = cdr(sub_args)
        args = cdr(args)
    body = lmbd.body
    return eval_lisp(body, se)


def macro_expand(body, e):
    type = get_type(body)
    if type == 'ConsList':
        return cons(macro_expand(car(body), e), macro_expand(cdr(body), e))
    if type == 'Symbol':
        return eval_symbol(body, e)
    return body


def eval_macro(mcr, args, e):
    sub_args = mcr.args
    se = sub_env(e)
    while not is_empty(sub_args):
        if is_empty(args):
            raise Exception('not enough args!')
        arg = car(args)
        k = get_value(car(sub_args))
        def_env(se, k, arg)
        sub_args = cdr(sub_args)
        args = cdr(args)
    body = macro_expand(mcr.body, se)
    return eval_lisp(body, e)


def eval_symbol(s, e):
    t = get_type(s)
    if t != 'Symbol':
        raise Exception('{} is not a Symbol'.format(t))
    return get_env(e, s)


def eval_lisp(l, e):
    type = get_type(l)

    if type == 'ConsList':
        if is_empty(l):
            return l

        head_form = eval_lisp(car(l), e)
        tail = cdr(l)
        if head_form == OK_symbol:
            res = eval_lisp(tail, e)
            return res
        head_form_type = get_type(head_form)
        if head_form_type == 'BinOp':
            res = eval_bin_op(head_form, tail, e)
            return res
        if head_form_type == 'PredOp':
            res = eval_pred_op(head_form, tail, e)
            return res
        if head_form_type == 'SpecialForm':
            res = eval_special_form(head_form, tail, e)
            return res
        if head_form_type == 'Symbol':
            res = eval_symbol(head_form, e)
            return res
        if head_form_type == 'Lambda':
            res = eval_lambda(head_form, tail, e)
            return res
        if head_form_type == 'Macro':
            res = eval_macro(head_form, tail, e)
            return res
        return head_form
    if type == 'Symbol':
        if get_value(l) == 'None':
            return None
        return eval_symbol(l, e)
    return l


def eval_lispy(parsed):
    e = Env()
    try:
        res = show(eval_lisp(parsed, e))
        return res, None
    except Exception as err:
        return None, err
