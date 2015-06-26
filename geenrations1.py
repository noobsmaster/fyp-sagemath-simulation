g_size=8
G=MatrixSpace(GF(2),g_size,g_size)
for j in g_size
	for i in g_size
		G[i][j]=random.gf2()

G
