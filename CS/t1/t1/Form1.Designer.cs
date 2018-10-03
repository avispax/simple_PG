namespace t1
{
    partial class Form1
    {
        /// <summary>
        /// 必要なデザイナー変数です。
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// 使用中のリソースをすべてクリーンアップします。
        /// </summary>
        /// <param name="disposing">マネージド リソースを破棄する場合は true を指定し、その他の場合は false を指定します。</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows フォーム デザイナーで生成されたコード

        /// <summary>
        /// デザイナー サポートに必要なメソッドです。このメソッドの内容を
        /// コード エディターで変更しないでください。
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Form1));
            this.p1 = new System.Windows.Forms.PictureBox();
            this.button1 = new System.Windows.Forms.Button();
            this.nu1 = new System.Windows.Forms.NumericUpDown();
            this.nu2 = new System.Windows.Forms.NumericUpDown();
            ((System.ComponentModel.ISupportInitialize)(this.p1)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.nu1)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.nu2)).BeginInit();
            this.SuspendLayout();
            // 
            // p1
            // 
            this.p1.Image = ((System.Drawing.Image)(resources.GetObject("p1.Image")));
            this.p1.Location = new System.Drawing.Point(12, 12);
            this.p1.Name = "p1";
            this.p1.Size = new System.Drawing.Size(252, 154);
            this.p1.SizeMode = System.Windows.Forms.PictureBoxSizeMode.Zoom;
            this.p1.TabIndex = 0;
            this.p1.TabStop = false;
            this.p1.Click += new System.EventHandler(this.pictureBox1_Click);
            // 
            // button1
            // 
            this.button1.Location = new System.Drawing.Point(334, 118);
            this.button1.Name = "button1";
            this.button1.Size = new System.Drawing.Size(279, 48);
            this.button1.TabIndex = 1;
            this.button1.Text = "button1";
            this.button1.UseVisualStyleBackColor = true;
            this.button1.Click += new System.EventHandler(this.button1_Click);
            // 
            // nu1
            // 
            this.nu1.Location = new System.Drawing.Point(334, 38);
            this.nu1.Name = "nu1";
            this.nu1.Size = new System.Drawing.Size(120, 19);
            this.nu1.TabIndex = 2;
            // 
            // nu2
            // 
            this.nu2.Location = new System.Drawing.Point(334, 63);
            this.nu2.Name = "nu2";
            this.nu2.Size = new System.Drawing.Size(120, 19);
            this.nu2.TabIndex = 3;
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(800, 450);
            this.Controls.Add(this.nu2);
            this.Controls.Add(this.nu1);
            this.Controls.Add(this.button1);
            this.Controls.Add(this.p1);
            this.Name = "Form1";
            this.Text = "Form1";
            ((System.ComponentModel.ISupportInitialize)(this.p1)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.nu1)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.nu2)).EndInit();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.PictureBox p1;
        private System.Windows.Forms.Button button1;
        private System.Windows.Forms.NumericUpDown nu1;
        private System.Windows.Forms.NumericUpDown nu2;
    }
}

