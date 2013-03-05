def stirling2(n,k): 
	"""Returns the stirling number Stirl2(n,k) of the second kind using recursion.""" 
	if k <= 1 or k == n: 
		return 1L
	if k > n or n <= 0: 
		return 0L 

	return stirling2(n-1, k-1) + k * stirling2(n-1, k) 

print stirling2(4,2)
