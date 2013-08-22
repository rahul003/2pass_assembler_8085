Imports System.Diagnostics.Process

Public Class Form1


    Private Sub Button1_Click(ByVal sender As System.Object, ByVal e As System.EventArgs)


    End Sub

    Public Sub Form1_Load(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles MyBase.Load

        Dim FileName As String = "C:\Users\Magneto\Desktop\8085\instructions"
        Dim myarray() As String = System.IO.File.ReadAllLines(FileName)
        ComboBox1.Items.AddRange(myarray)
    End Sub

    Dim arg1 As String

    Private Sub Button2_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button2.Click
        SaveFileDialog1.ShowDialog()
        My.Computer.FileSystem.WriteAllText(SaveFileDialog1.FileName, TextBox1.Text, False)
        arg1 = SaveFileDialog1.FileName
        MessageBox.Show(arg1.ToString)
        'Dim compiler As String = "C:\\Python27\python.exe"
        'Dim filename As String = "C:\\Users\Magneto\Desktop\8085\mnem8am.py"
        'Dim name As String = "C:\\Users\Magneto\Desktop\8085\rand none 0"
        'Shell("C:\\Python27\python.exe C:\\Users\Magneto\Desktop\8085\mnem8am.py C:\Users\Magneto\Desktop\8085\rand none 0")
        Shell("cmd.exe /c " & compiler &" " filename & " " & name, vbNormalFocus)
        Threading.Thread.Sleep(2000)
        TextBox4.Text = System.IO.File.ReadAllText("C:\\Users\Magneto\Desktop\8085\err")
        MsgBox("ok")

        '       Console.
        ' Shell("python print.py")
        ' Shell("cmd.exe")

    End Sub



    Private Sub Button3_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button3.Click
        TextBox3.Text = Hex(TextBox2.Text)
    End Sub

    Private Sub Button4_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button4.Click
        TextBox3.Text = CLng("&H" & TextBox2.Text)
    End Sub

    Private Sub Button1_Click_1(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button1.Click
        TextBox1.AppendText(ComboBox1.SelectedItem)
    End Sub

    Private Sub Button5_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button5.Click
        TextBox1.AppendText(ComboBox2.SelectedItem)
    End Sub

    Dim tmpword As String

    Private Sub TextBox1_TextChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles TextBox1.TextChanged

    End Sub

    

    Private Sub Button6_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button6.Click
        SaveFileDialog1.ShowDialog()
        My.Computer.FileSystem.WriteAllText(SaveFileDialog1.FileName+".txt", TextBox1.Text, False)
    End Sub

    Private Sub Button7_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button7.Click
        OpenFileDialog1.ShowDialog()
        TextBox1.Text = System.IO.File.ReadAllText(OpenFileDialog1.FileName)
    End Sub

    Dim arg2 As String

    Private Sub CheckBox1_CheckedChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles CheckBox1.CheckedChanged
        OpenFileDialog2.ShowDialog()
        arg2 = OpenFileDialog2.FileName
    End Sub

End Class
