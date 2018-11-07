using System;
using System.Collections.Generic;
using System.Linq;
using System.ServiceModel;
using System.ServiceModel.Channels;
using System.Text;
using System.Threading.Tasks;
using testForm.psx;

namespace testForm
{
    class Class2 : psx.PSXAPI_r11_00_00
    {

    }

    class Class1 : psx.PSXAPI_r11_00_00Channel
    {
        bool IClientChannel.AllowInitializationUI { get => throw new NotImplementedException(); set => throw new NotImplementedException(); }

        bool IClientChannel.DidInteractiveInitialization => throw new NotImplementedException();

        Uri IClientChannel.Via => throw new NotImplementedException();

        bool IContextChannel.AllowOutputBatching { get => throw new NotImplementedException(); set => throw new NotImplementedException(); }

        IInputSession IContextChannel.InputSession => throw new NotImplementedException();

        EndpointAddress IContextChannel.LocalAddress => throw new NotImplementedException();

        TimeSpan IContextChannel.OperationTimeout { get => throw new NotImplementedException(); set => throw new NotImplementedException(); }

        IOutputSession IContextChannel.OutputSession => throw new NotImplementedException();

        EndpointAddress IContextChannel.RemoteAddress => throw new NotImplementedException();

        string IContextChannel.SessionId => throw new NotImplementedException();

        CommunicationState ICommunicationObject.State => throw new NotImplementedException();

        IExtensionCollection<IContextChannel> IExtensibleObject<IContextChannel>.Extensions => throw new NotImplementedException();

        event EventHandler<UnknownMessageReceivedEventArgs> IClientChannel.UnknownMessageReceived
        {
            add
            {
                throw new NotImplementedException();
            }

            remove
            {
                throw new NotImplementedException();
            }
        }

        event EventHandler ICommunicationObject.Closed
        {
            add
            {
                throw new NotImplementedException();
            }

            remove
            {
                throw new NotImplementedException();
            }
        }

        event EventHandler ICommunicationObject.Closing
        {
            add
            {
                throw new NotImplementedException();
            }

            remove
            {
                throw new NotImplementedException();
            }
        }

        event EventHandler ICommunicationObject.Faulted
        {
            add
            {
                throw new NotImplementedException();
            }

            remove
            {
                throw new NotImplementedException();
            }
        }

        event EventHandler ICommunicationObject.Opened
        {
            add
            {
                throw new NotImplementedException();
            }

            remove
            {
                throw new NotImplementedException();
            }
        }

        event EventHandler ICommunicationObject.Opening
        {
            add
            {
                throw new NotImplementedException();
            }

            remove
            {
                throw new NotImplementedException();
            }
        }

        void ICommunicationObject.Abort()
        {
            throw new NotImplementedException();
        }

        IAsyncResult ICommunicationObject.BeginClose(AsyncCallback callback, object state)
        {
            throw new NotImplementedException();
        }

        IAsyncResult ICommunicationObject.BeginClose(TimeSpan timeout, AsyncCallback callback, object state)
        {
            throw new NotImplementedException();
        }

        IAsyncResult IClientChannel.BeginDisplayInitializationUI(AsyncCallback callback, object state)
        {
            throw new NotImplementedException();
        }

        IAsyncResult ICommunicationObject.BeginOpen(AsyncCallback callback, object state)
        {
            throw new NotImplementedException();
        }

        IAsyncResult ICommunicationObject.BeginOpen(TimeSpan timeout, AsyncCallback callback, object state)
        {
            throw new NotImplementedException();
        }

        void PSXAPI_r11_00_00.bulkDelete()
        {
            throw new NotImplementedException();
        }

        void PSXAPI_r11_00_00.bulkDeleteAsync()
        {
            throw new NotImplementedException();
        }

        void PSXAPI_r11_00_00.bulkRetrieve()
        {
            throw new NotImplementedException();
        }

        void PSXAPI_r11_00_00.bulkRetrieveAsync()
        {
            throw new NotImplementedException();
        }

        void PSXAPI_r11_00_00.bulkUpdate()
        {
            throw new NotImplementedException();
        }

        void PSXAPI_r11_00_00.bulkUpdateAsync()
        {
            throw new NotImplementedException();
        }

        void ICommunicationObject.Close()
        {
            throw new NotImplementedException();
        }

        void ICommunicationObject.Close(TimeSpan timeout)
        {
            throw new NotImplementedException();
        }

        void PSXAPI_r11_00_00.create()
        {
            throw new NotImplementedException();
        }

        void PSXAPI_r11_00_00.create1()
        {
            throw new NotImplementedException();
        }

        void PSXAPI_r11_00_00.create1Async()
        {
            throw new NotImplementedException();
        }

        void PSXAPI_r11_00_00.createAsync()
        {
            throw new NotImplementedException();
        }

        void PSXAPI_r11_00_00.delete()
        {
            throw new NotImplementedException();
        }

        void PSXAPI_r11_00_00.delete1()
        {
            throw new NotImplementedException();
        }

        void PSXAPI_r11_00_00.delete1Async()
        {
            throw new NotImplementedException();
        }

        void PSXAPI_r11_00_00.deleteAsync()
        {
            throw new NotImplementedException();
        }

        void IClientChannel.DisplayInitializationUI()
        {
            throw new NotImplementedException();
        }

        void IDisposable.Dispose()
        {
            throw new NotImplementedException();
        }

        void ICommunicationObject.EndClose(IAsyncResult result)
        {
            throw new NotImplementedException();
        }

        void IClientChannel.EndDisplayInitializationUI(IAsyncResult result)
        {
            throw new NotImplementedException();
        }

        void ICommunicationObject.EndOpen(IAsyncResult result)
        {
            throw new NotImplementedException();
        }

        void PSXAPI_r11_00_00.getCount()
        {
            throw new NotImplementedException();
        }

        void PSXAPI_r11_00_00.getCountAsync()
        {
            throw new NotImplementedException();
        }

        void PSXAPI_r11_00_00.getJobStatus()
        {
            throw new NotImplementedException();
        }

        void PSXAPI_r11_00_00.getJobStatusAsync()
        {
            throw new NotImplementedException();
        }

        void PSXAPI_r11_00_00.getNextItems()
        {
            throw new NotImplementedException();
        }

        void PSXAPI_r11_00_00.getNextItemsAsync()
        {
            throw new NotImplementedException();
        }

        T IChannel.GetProperty<T>()
        {
            throw new NotImplementedException();
        }

        void PSXAPI_r11_00_00.listall()
        {
            throw new NotImplementedException();
        }

        void PSXAPI_r11_00_00.listallAsync()
        {
            throw new NotImplementedException();
        }

        void ICommunicationObject.Open()
        {
            throw new NotImplementedException();
        }

        void ICommunicationObject.Open(TimeSpan timeout)
        {
            throw new NotImplementedException();
        }

        void PSXAPI_r11_00_00.put()
        {
            throw new NotImplementedException();
        }

        void PSXAPI_r11_00_00.put1()
        {
            throw new NotImplementedException();
        }

        void PSXAPI_r11_00_00.put1Async()
        {
            throw new NotImplementedException();
        }

        void PSXAPI_r11_00_00.putAsync()
        {
            throw new NotImplementedException();
        }

        void PSXAPI_r11_00_00.retrieve()
        {
            throw new NotImplementedException();
        }

        void PSXAPI_r11_00_00.retrieve1()
        {
            throw new NotImplementedException();
        }

        void PSXAPI_r11_00_00.retrieve1Async()
        {
            throw new NotImplementedException();
        }

        void PSXAPI_r11_00_00.retrieveAsync()
        {
            throw new NotImplementedException();
        }

        void PSXAPI_r11_00_00.update()
        {
            throw new NotImplementedException();
        }

        void PSXAPI_r11_00_00.update1()
        {
            throw new NotImplementedException();
        }

        void PSXAPI_r11_00_00.update1Async()
        {
            throw new NotImplementedException();
        }

        void PSXAPI_r11_00_00.updateAsync()
        {
            throw new NotImplementedException();
        }
    }
}
