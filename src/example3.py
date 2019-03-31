# coding=utf-8
"""
@author: zhang.pengfei5
@contact: zhang.pengfei5@iwhalecloud.com
@time: 2019/3/24 21:41
@description:
    根据 pdm 文件内容生成 Django的Model 文件
"""
from PDMHandler import PDMHandler

if __name__ == '__main__':
    filename = 'testpdm/project.pdm'
    ph = PDMHandler.parse(filename)
    for pkg in PDMHandler.getPkgNodes(ph):
        pkg_attrs = PDMHandler.getPkgAttrs(pkg)
        print("P:", pkg_attrs["Name"], pkg_attrs["Code"], pkg_attrs["Creator"])
        lines = ['from django.db import models\n']
        for tbl in PDMHandler.getTblNodesInPkg(pkg):
            tbl_attrs = PDMHandler.getTblAttrs(tbl)
            print(" T:", tbl_attrs["Name"], tbl_attrs["Code"], tbl_attrs["Creator"])
            print("  T-PATH:", PDMHandler.getNodePath(tbl))
            model = []
            model.append('class {table_name}(models.Model):'.format(table_name=tbl_attrs["Code"]))
            for col in PDMHandler.getColNodesInTbl(tbl):
                col_attrs = PDMHandler.getColAttrs(col)
                print("  C:", col_attrs["Name"], col_attrs["Code"], col_attrs["DataType"], col_attrs["Length"],
                      col_attrs["Column.Mandatory"])

                if 'char' in col_attrs["DataType"]:
                    column = '  {} = models.{}(max_length={})'.format(col_attrs["Code"], 'CharField',
                                                                      col_attrs["Length"])
                elif 'numeric' in col_attrs["DataType"]:
                    column = '  {} = models.{}()'.format(col_attrs["Code"], 'IntegerField')
                model.append(column)
            model.append('\n')
            lines.extend(model)

            for idx in PDMHandler.getIdxNodesInTbl(tbl):
                idx_attrs = PDMHandler.getIdxAttrs(idx)
                print("  I:", idx_attrs["Name"], idx_attrs["Code"], idx_attrs["Unique"])
                for idxcol in PDMHandler.getIdxColNodesInIdx(idx):
                    idxcol_attrs = PDMHandler.getIdxColAttrs(idxcol)
                    print("   IC:", idxcol_attrs["RefColCode"])

        with open('model.py', 'w') as f:
            f.write('\n'.join(lines))
