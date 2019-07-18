# import top_pkg.pkg_a.a_1
# from top_pkg.pkg_a import a_1
# import top_pkg
# top_pkg = __import__('top_pkg', globals(), locals(), [], 0)

# top_pkg = __import__('top_pkg.pkg_a', globals(), locals(), ['pkg_a'], 0)
# print(top_pkg)
# # from top_pkg.pkg_b import b_1, b_2
# _temp = __import__('top_pkg.pkg_b', globals(), locals(), ['b_1', 'b_2'], 0)
# b_1 = _temp.b_1
# b_2 = _temp.b_2
# print(b_1)

# pkg_a = __import__('top_pkg.pkg_a', globals(), locals(), ['pkg_a'], 0)
# print(pkg_a)
