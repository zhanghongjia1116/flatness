def get_K(policyNo, data, data_CPB, data_CPL):
    # data_CPB = pd.read_excel('CPB.xlsx', header=None)
    # data_CPL = pd.read_excel('CPL.xlsx', header=None)
    policyNo = int(policyNo)
    # data = pd.read_excel('待评价工况.xlsx')
    row_data = data[data['ID'] == policyNo]

    n = row_data.index[0]
    CPtarget = row_data.iloc[0, 18]  # 目标凸度
    C40base = row_data.iloc[0, 17]  # 来料凸度
    CPL = data_CPL.iloc[n, :]
    CPB = data_CPB.iloc[n, :]
    xiuzheng = [150, 150, 150, 150, 100]  # 凸度修正量

    K1 = 0
    # temp_CPL = np.concatenate(C40base, CPL + xiuzheng)
    temp_CPL = [C40base] + list(CPL + xiuzheng)
    temp_CPtarget = CPtarget  # 目标比例凸度
    for S in range(4):
        if abs(temp_CPL[S] - temp_CPtarget) > abs(temp_CPL[S + 1] - temp_CPtarget):
            K1 += 1
    K1 /= 5

    K2 = 0
    temp_CPL = CPL + xiuzheng
    temp_CPB = CPB + xiuzheng
    temp_CPtarget = CPtarget
    for S in range(4):
        if abs(temp_CPL[S] - temp_CPtarget) > abs(temp_CPB[S] - temp_CPtarget):
            K2 += 1
    K2 /= 5

    K3 = 0
    # temp_CPL = np.concatenate((CPL.iloc[n, :] + xiuzheng, [CPtarget[n]]))  # 加入目标凸度
    temp_CPL = [CPL + xiuzheng] + CPtarget
    # 二维数组变为一维数组
    temp_CPL = temp_CPL.flatten()
    temp_CPtarget = CPtarget
    for S in range(4):
        K3 += abs(temp_CPL[S] - temp_CPL[S + 1])
    if abs(K3) < 1:
        K3 = 0.5
    else:
        K3 = abs(temp_CPL[0] - temp_CPtarget)
    K3 /= 5

    K = K1 + K2 + K3
    return K
