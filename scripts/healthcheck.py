from steam import game_servers as gs
res = gs.a2s_info(('172.17.0.2', 2457))
print("DOCKER:", res)
res_localhost = gs.a2s_info(('localhost', 2457))
print("LOCALHOST:", res_localhost)
res_realip = gs.a2s_info(('ood.sh', 2457))
print("REAL IP:", res_realip)
